from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.exchange_oex.rest.rest_base import ExchangeRestApi, ExchangeRestService

from ..models.valuations import GetValuationsRequestParams, GetValuationsResponse


class GetValuationsApi(ExchangeRestApi):
    """Fetches certain valuation type data for a particular instrument."""

    path = "public/get-valuations"
    method = HttpMethods.GET
    request_params_type = GetValuationsRequestParams
    response_type = GetValuationsResponse


class ValuationsService(ExchangeRestService):
    def get_valuations(
        self,
        instrument_name: str,
        valuation_type: str,
        count: int = None,
        start_ts: int = None,
        end_ts: int = None,
    ) -> GetValuationsResponse:
        """
        To request the api: /public/get-valuations

        @param instrument_name: BTC_USD-PERP or BTC_USD Index
        @param valuation_type: index_price, funding_rate,mark_price
        @param count: Return the data row count
        @param start_ts: start time
        @param end_ts: end time
        @return: GetValuationsResponse
        """
        api = GetValuationsApi(host=self.host, _session=self.session)
        params = GetValuationsRequestParams(
            instrument_name=instrument_name,
            valuation_type=valuation_type,
            count=count,
            start_ts=start_ts,
            end_ts=end_ts,
        ).dict(exclude_none=True)
        response = GetValuationsResponse.parse_raw(b=api.call(params=params).content)

        return response
