from typing import Union
from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.exchange.rest.rest_base import ExchangeRestApi, ExchangeRestService

from ..models.ticker import (
    GetTickerRequestParams,
    GetTickerResponse,
    GetAllTickersResponse,
)


class GetTickerApi(ExchangeRestApi):
    """exchange-public get ticker"""

    path = "public/get-ticker"
    method = HttpMethods.GET
    request_params_type = GetTickerRequestParams
    response_type = GetTickerResponse


class TickerService(ExchangeRestService):
    def get_ticker(self, instrument_name: str = None) -> Union[GetAllTickersResponse, GetTickerResponse]:
        api = GetTickerApi(host=self.host, _session=self.session)
        params = GetTickerRequestParams(instrument_name=instrument_name).dict(exclude_none=True)
        response = GetTickerResponse.parse_raw(b=api.call(params=params).content)
        return response
