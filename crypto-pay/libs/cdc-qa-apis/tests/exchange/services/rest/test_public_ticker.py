from cdc.qa.apis import exchange
from .mocks import *  # noqa


def test_rest_public_ticker_service_get(mock_get_ticker_btc_usdt):

    api = exchange.rest.public.TickerService(api_key="", secret_key="", host="https://uat-api.3ona.co/v2/")
    result = api.get_ticker(instrument_name="BTC_USDT").result

    assert result.data[0].i == "BTC_USDT"


def test_rest_public_ticker_service_get_all(mock_get_ticker):
    api = exchange.rest.public.TickerService(api_key="", secret_key="", host="https://uat-api.3ona.co/v2/")
    result = api.get_ticker().result

    assert result.data[0].i == "VET_BTC"
