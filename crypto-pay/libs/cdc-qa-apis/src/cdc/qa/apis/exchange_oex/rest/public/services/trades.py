from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.exchange_oex.rest.rest_base import ExchangeRestApi, ExchangeRestService

from ..models.trades import GetTradesRequestParams, GetTradesResponse


class GetTradesApi(ExchangeRestApi):
    """exchange-public get trades"""

    path = "public/get-trades"
    method = HttpMethods.GET
    request_params_type = GetTradesRequestParams
    response_type = GetTradesResponse


class TradesService(ExchangeRestService):
    def get_trades(
        self, instrument_name: str, count: int = None, start_ts: int = None, end_ts: int = None
    ) -> GetTradesResponse:
        api = GetTradesApi(host=self.host, _session=self.session)
        params = GetTradesRequestParams(
            instrument_name=instrument_name,
            count=count,
            start_ts=start_ts,
            end_ts=end_ts,
        ).dict(exclude_none=True)
        response = GetTradesResponse.parse_raw(b=api.call(params=params).content)
        return response
