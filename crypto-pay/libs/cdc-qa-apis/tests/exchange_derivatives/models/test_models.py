import json
import pytest
from cdc.qa.apis.exchange_derivatives.models import DerivativesRequest, DerivativesSignedRequest
from cdc.qa.apis.exchange_derivatives.rest.private.models.orders import CreateOrderResponse
from pydantic import BaseModel
from pydantic.error_wrappers import ValidationError


def test_generate_signature():
    class ParamsModel(BaseModel):
        some_param: str
        another_param: int

    request = DerivativesSignedRequest(
        id=101,
        method="test/method",
        params=ParamsModel(some_param="abc", another_param=123),
        nonce=123456789,
        api_key="api",
        secret_key="secret",
    )

    assert request.sig == "49948da1a0d13bd2f256e1680245b27b310ccafe9bc313824898ccc90c2b56af"


def test_fixed_signature():
    class ParamsModel(BaseModel):
        some_param: str
        another_param: int

    request = DerivativesSignedRequest(
        id=101,
        method="test/method",
        params=ParamsModel(some_param="abc", another_param=123),
        nonce=123456789,
        api_key="api",
        secret_key="secret",
        sig="fix_sig",
    )

    assert request.sig == "fix_sig"


def test_validate_success():
    obj = {"method": "some/method"}
    assert DerivativesRequest.validate(obj)


def test_validate_fail():
    obj = {"missing": "value"}
    with pytest.raises(ValidationError):
        DerivativesRequest.validate(obj)


def test_pydantic_parse_raw_with_exception():
    obj = json.dumps(
        {"id": 1, "code": 315, "message": "FAR_AWAY_LIMIT_PRICE", "result": {"client_oid": "1", "order_id": 8534}}
    ).encode()
    with pytest.raises(ValidationError) as execinfo:
        CreateOrderResponse.parse_raw(b=obj)
    raw_errors = execinfo.value.raw_errors
    value_error = [
        error
        for error in raw_errors
        if (not isinstance(error, list))
        and isinstance(error.exc, ValueError)
        and "original content:" in error.loc_tuple()
    ][0]
    error_info = json.loads(value_error.exc.args[0])
    assert error_info.get("message") == "FAR_AWAY_LIMIT_PRICE"
    assert error_info.get("code") == 315


def test_pydantic_parse_raw_without_exception():
    obj = json.dumps(
        {"id": 123, "method": "private/create-order", "code": 0, "result": {"client_oid": "123", "order_id": 8529}}
    ).encode()
    resp = CreateOrderResponse.parse_raw(b=obj)
    assert resp.result.client_oid == "123"
    assert resp.code == 0
    assert resp.result.order_id == 8529
