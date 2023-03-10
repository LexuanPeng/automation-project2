import json

from cdc.qa.apis import exchange
from .mocks import *  # noqa


def test_use_api_from_exchange_api(mock_get_instruments):
    exchange_api = exchange.ExchangeApi(api_key="", secret_key="")
    instruments = exchange_api.rest.public.instruments.get_instruments().result.instruments

    assert instruments[0].instrument_name == "SHIB_USDT"


def test_use_api_from_exchange_rest_services(mock_get_instruments):
    exchange_rest_services = exchange.rest.ExchangeRestServices(api_key="", secret_key="")
    instruments = exchange_rest_services.public.instruments.get_instruments().result.instruments

    assert instruments[0].instrument_name == "SHIB_USDT"


def test_use_api_from_public_services(mock_get_instruments):
    public_services = exchange.rest.public.PublicServices(
        host="https://uat-api.3ona.co/v2/",
        api_key="",
        secret_key="",
    )
    instruments = public_services.instruments.get_instruments().result.instruments

    assert instruments[0].instrument_name == "SHIB_USDT"


def test_use_api_from_get_instruments_service(mock_get_instruments):
    get_instruments_service = exchange.rest.public.InstrumentsService(
        host="https://uat-api.3ona.co/v2/",
        api_key="",
        secret_key="",
    )
    instruments = get_instruments_service.get_instruments().result.instruments

    assert instruments[0].instrument_name == "SHIB_USDT"


def test_use_api_from_get_instruments_api(mock_get_instruments):
    api = exchange.rest.public.GetInstrumentsApi(host="https://uat-api.3ona.co/v2/")
    instruments = json.loads(api.call().content).get("result").get("instruments")

    assert instruments[0].get("instrument_name") == "SHIB_USDT"
