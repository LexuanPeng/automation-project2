from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.exchange.rest.rest_base import ExchangeRestApi, ExchangeRestService

from ..models.trades import (
    GetTradesRequestBody,
    GetTradesRequestParams,
    GetTradesResponse,
)


class GetTradesApi(ExchangeRestApi):
    """exchange-private deriv get trades"""

    path = "private/get-trades"
    method = HttpMethods.POST
    request_data_type = GetTradesRequestBody
    response_type = GetTradesResponse


class TradesService(ExchangeRestService):
    def get_trades(
        self,
        instrument_name: str = None,
        start_ts: int = None,
        end_ts: int = None,
        page_size: int = None,
        page: int = None,
    ) -> GetTradesResponse:
        """request get trades
        Args:
            instrument_name: e.g. ETH_CRO, BTC_USDT. Omit for 'all'
            start_ts: Start timestamp (milliseconds since the Unix epoch) - defaults to 24 hours ago
            end_ts: End timestamp (milliseconds since the Unix epoch) - defaults to 'now'
            page_size: Page size (Default: 20, max: 200)
            page: Page number (0-based)

        Returns:
            GetTradesResponse
        """
        params = {
            "instrument_name": instrument_name,
            "start_ts": start_ts,
            "end_ts": end_ts,
            "page_size": page_size,
            "page": page,
        }
        api = GetTradesApi(host=self.host, _session=self.session)
        payload = GetTradesRequestBody(
            params=GetTradesRequestParams(**params), api_key=self.api_key, secret_key=self.secret_key
        ).json(exclude_none=True)
        response = GetTradesResponse.parse_raw(b=api.call(data=payload).content)
        return response
