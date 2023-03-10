from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.exchange_derivatives.rest.rest_base import DerivativesRestApi, DerivativesRestService

from ..models.ticker import (
    GetTickersRequestParams,
    GetTickersResponse,
)


class GetTickersApi(DerivativesRestApi):
    """Fetches the public tickers for all or a particular instrument."""

    path = "public/get-tickers"
    method = HttpMethods.GET
    request_params_type = GetTickersRequestParams
    response_type = GetTickersResponse


class TickerService(DerivativesRestService):
    def get_tickers(self, instrument_name: str = None) -> GetTickersResponse:
        api = GetTickersApi(host=self.host, _session=self.session)
        params = GetTickersRequestParams(instrument_name=instrument_name).dict(exclude_none=True)
        response = GetTickersResponse.parse_raw(b=api.call(params=params).content)

        return response
