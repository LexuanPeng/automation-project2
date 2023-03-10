from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.exchange.rest.rest_base import ExchangeRestApi, ExchangeRestService

from ..models.trades import GetTradesRequestParams, GetTradesResponse


class GetTradesApi(ExchangeRestApi):
    """exchange-public get trades"""

    path = "public/get-trades"
    method = HttpMethods.GET
    request_params_type = GetTradesRequestParams
    response_type = GetTradesResponse


class TradesService(ExchangeRestService):
    def get_trades(self, instrument_name: str = None, size: int = None) -> GetTradesResponse:
        api = GetTradesApi(host=self.host, _session=self.session)
        params = GetTradesRequestParams(instrument_name=instrument_name, size=size).dict(exclude_none=True)
        response = GetTradesResponse.parse_raw(b=api.call(params=params).content)
        return response
