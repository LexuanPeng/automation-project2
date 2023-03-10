from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.exchange_oex.rest.rest_base import ExchangeRestApi, ExchangeRestService

from ..models.candlestick import GetCandlestickRequestParams, GetCandlestickResponse


class GetCandlestickApi(ExchangeRestApi):
    """public get candlestick"""

    path = "public/get-candlestick"
    method = HttpMethods.GET
    request_params_type = GetCandlestickRequestParams
    response_type = GetCandlestickResponse


class CandlestickService(ExchangeRestService):
    def get_candlestick(
        self,
        instrument_name: str,
        timeframe: str = None,
        count: int = None,
        start_ts: int = None,
        end_ts: int = None,
    ) -> GetCandlestickResponse:
        api = GetCandlestickApi(host=self.host, _session=self.session)
        params = GetCandlestickRequestParams(
            instrument_name=instrument_name,
            timeframe=timeframe,
            count=count,
            start_ts=start_ts,
            end_ts=end_ts,
        ).dict(exclude_none=True)
        response = GetCandlestickResponse.parse_raw(b=api.call(params=params).content)

        return response
