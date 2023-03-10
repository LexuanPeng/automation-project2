import json

from cdc.qa.apis import exchange
from .mocks import *  # noqa


def test_rest_public_get_trades_api(mock_get_trades):
    api = exchange.rest.public.GetTradesApi(host="https://uat-api.3ona.co/v2/")
    params = exchange.rest.public.GetTradesApi.request_params_type(instrument_name="ICX_CRO")
    data = json.loads(api.call(params=params).content).get("result").get("data")

    assert data[0].get("i") == "ICX_CRO"
