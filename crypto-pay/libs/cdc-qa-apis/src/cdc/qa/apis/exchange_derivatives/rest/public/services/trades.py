from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.exchange_derivatives.rest.rest_base import DerivativesRestApi, DerivativesRestService

from ..models.trades import GetTradesRequestParams, GetTradesResponse


class GetTradesApi(DerivativesRestApi):
    """Fetches the public trades for a particular instrument."""

    path = "public/get-trades"
    method = HttpMethods.GET
    request_params_type = GetTradesRequestParams
    response_type = GetTradesResponse


class TradesService(DerivativesRestService):
    def get_trades(self, instrument_name: str, count: int = None) -> GetTradesResponse:
        api = GetTradesApi(host=self.host, _session=self.session)
        params = GetTradesRequestParams(instrument_name=instrument_name, count=count).dict(exclude_none=True)
        response = GetTradesResponse.parse_raw(b=api.call(params=params).content)

        return response
