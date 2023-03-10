from cdc.qa.apis import exchange_derivatives
import pytest
from .mocks import *  # noqa


@pytest.fixture
def instrument_service():
    service = exchange_derivatives.rest.public.InstrumentsService(
        api_key="", secret_key="", host="https://dstg-rest-gateway.x.3ona.co/deriv/v1/"
    )
    return service


def test_get_beta_instruments(instrument_service, mock_get_beta_instruments):
    response = instrument_service.get_beta_instruments()
    data_result = response.result.data[0]
    assert data_result.symbol == "BTCUSD-211227-CW43000"
    assert not data_result.tradable
    assert data_result.beta_product
    assert data_result.quote_decimals == 3
