import pytest
import json
from cdc.qa.apis.exchange.models import ExchangeRequest, ExchangeSignedRequest
from pydantic import BaseModel, Field
from pydantic.error_wrappers import ValidationError
from decimal import Decimal
from typing import Union
from cdc.qa.apis.exchange.rest.private.models.orders import CreateOrderResponse
from cdc.qa.apis.exchange.rest.private.models.account import AccountDetail


def test_generate_signature():
    class ParamsModel(BaseModel):
        some_param: str
        another_param: int

    request = ExchangeSignedRequest(
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

    request = ExchangeSignedRequest(
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
    assert ExchangeRequest.validate(obj)


def test_validate_fail():
    obj = {"missing": "value"}
    with pytest.raises(ValidationError):
        ExchangeRequest.validate(obj)


@pytest.mark.parametrize(
    ["amount", "sign"],
    [
        (0.028, "b6897e4c43ca925d59c1ee01e37fb453400bc9baf3c921f6eab0f9b9f1de0922"),
        (0.0280, "b6897e4c43ca925d59c1ee01e37fb453400bc9baf3c921f6eab0f9b9f1de0922"),
        (2, "2ae0280fcd5d3232f01a1eb58dce3ef148fe9549ffa14be1b844c63764376b00"),
        (2.0, "b008deecc4165e63590fccd5d54918cbfa2512b0fb7412cd3a01329460e117ac"),
        (Decimal("0.028"), "b6897e4c43ca925d59c1ee01e37fb453400bc9baf3c921f6eab0f9b9f1de0922"),
        (Decimal("0.0280"), "93ef0435ee5d2a81fa743aaf83fa5aa931334fade8eaceeef5ad7a59b794243c"),
        ("0.028", "b6897e4c43ca925d59c1ee01e37fb453400bc9baf3c921f6eab0f9b9f1de0922"),
    ],
)
def test_alias_field_signature(amount, sign):
    class DerivTransferRequestParams(BaseModel):
        currency: str = Field(description="Transfer currency, e.g. BTC, CRO")
        from_side: str = Field(description="SPOT or DERIVATIVES", alias="from")
        to: str = Field(description="SPOT or DERIVATIVES")
        amount: Union[str, Decimal, int] = Field(description="The amount to be transferred")

    params = {"currency": "USDC", "from": "SPOT", "to": "DERIVATIVES", "amount": amount}
    request = ExchangeSignedRequest(
        id=5276345,
        method="private/deriv/transfer",
        params=DerivTransferRequestParams(**params),
        nonce="1625107370552",
        api_key="api",
        secret_key="secret",
    )

    assert request.sig == sign


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


def test_pydantic_parse_float():
    obj = b"""{
        "balance": 19999999898.017928000000000000,
        "available": 19999999898.017928000000000000,
        "order": 0,
        "stake": 0,
        "currency": "LTC"
    }"""

    detail = AccountDetail.parse_raw(b=obj)
    assert detail.balance == Decimal("19999999898.017928000000000000")
