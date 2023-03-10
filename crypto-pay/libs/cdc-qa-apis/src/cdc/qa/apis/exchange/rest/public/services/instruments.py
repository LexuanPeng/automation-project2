from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.exchange.rest.rest_base import ExchangeRestApi, ExchangeRestService

from ..models.instruments import GetInstrumentsResponse


class GetInstrumentsApi(ExchangeRestApi):
    """Provides information on all supported instruments (e.g. BTC_USDT)"""

    path = "public/get-instruments"
    method = HttpMethods.GET
    response_type = GetInstrumentsResponse


class InstrumentsService(ExchangeRestService):
    def get_instruments(self) -> GetInstrumentsResponse:
        api = GetInstrumentsApi(host=self.host, _session=self.session)
        response = GetInstrumentsResponse.parse_raw(b=api.call().content)

        return response
