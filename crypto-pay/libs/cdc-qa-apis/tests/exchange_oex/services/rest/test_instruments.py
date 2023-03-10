import pytest
from cdc.qa.apis import exchange_oex
from .mocks import *  # noqa


@pytest.fixture
def instruments_services():
    services = exchange_oex.rest.public.InstrumentsService(
        api_key="", secret_key="", host="https://dstg-rest-gateway.x.3ona.co/v1/"
    )
    return services


def test_get_instruments(instruments_services, mock_get_instruments):
    response = instruments_services.get_instruments()
    data_result = response.result.data[0]
    assert data_result.symbol == "BTCUSD-221028"
    assert not data_result.tradable
    assert not data_result.beta_product
    assert data_result.quote_decimals == 1
