import logging
from typing import Optional

from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.rails.models.target_price import (
    MarketPriceQueryParams,
    MarketPriceResponse,
    TargetPriceOrderQuotationRequestData,
    TargetPriceOrderQuotationResponse,
    TargetPriceOrderCreateRequestData,
    TargetPriceOrderCreateResponse,
    TargetPriceOrderQueryParams,
    TargetPriceOrderResponse,
)
from ..models import RailsRestApi, RailsRestService

logger = logging.getLogger(__name__)

LIMIT_ORDER_HOST = "https://limit-order.3ona.co"
DEV_LIMIT_ORDER_HOST = "https://adev-limit-order.3ona.co"


class MarketPriceApi(RailsRestApi):
    """Get market price by base and quote currency"""

    path = "/api/v1/market_prices"
    method = HttpMethods.GET
    request_params_type = MarketPriceQueryParams
    response_type = MarketPriceResponse


class TargetPriceOrderQuotationApi(RailsRestApi):
    """Create Order Quotation"""

    path = "/api/v1/order_quotations"
    method = HttpMethods.POST
    request_data_type = TargetPriceOrderQuotationRequestData
    response_type = TargetPriceOrderQuotationResponse


class TargetPriceOrderCreateApi(RailsRestApi):
    """Create Order"""

    path = "/api/v1/orders"
    method = HttpMethods.POST
    request_data_type = TargetPriceOrderCreateRequestData
    response_type = TargetPriceOrderCreateResponse


class TargetPriceOrderIndexApi(RailsRestApi):
    """Get target orders"""

    path = "/api/v1/orders"
    method = HttpMethods.GET
    request_params_type = TargetPriceOrderQueryParams
    response_type = TargetPriceOrderResponse


class TargetPriceService(RailsRestService):
    def get_market_price(self, base_currency: str, quote_currency: str) -> MarketPriceResponse:
        api = MarketPriceApi(host=self._limit_host_, _session=self.session)
        params = MarketPriceQueryParams(base_currency=base_currency, quote_currency=quote_currency).dict(
            exclude_none=True
        )

        response = api.call(params=params)
        return MarketPriceResponse.parse_raw(b=response.content)

    def create_order_quotation(
        self,
        side: str,
        base_currency: str,
        base_amount: str,
        quote_currency: str,
        quote_price: str,
    ) -> TargetPriceOrderQuotationResponse:
        api = TargetPriceOrderQuotationApi(host=self._limit_host_, _session=self.session)
        data = TargetPriceOrderQuotationRequestData(
            side=side,
            base_currency=base_currency,
            base_amount=base_amount,
            quote_currency=quote_currency,
            quote_price=quote_price,
        ).dict(exclude_none=True)

        response = api.call(data=data)
        return TargetPriceOrderQuotationResponse.parse_raw(b=response.content)

    def create_order(
        self,
        passcode: str,
        external_id: str,
        order_quotation_token: str,
    ) -> TargetPriceOrderCreateResponse:
        api = TargetPriceOrderCreateApi(host=self._limit_host_, _session=self.session)
        data = TargetPriceOrderCreateRequestData(
            passcode=passcode,
            external_id=external_id,
            order_quotation_token=order_quotation_token,
        ).dict(exclude_none=True)

        response = api.call(data=data)
        return TargetPriceOrderCreateResponse.parse_raw(b=response.content)

    def get_orders(self, count: Optional[int] = 10, state: Optional[str] = "open") -> TargetPriceOrderResponse:
        api = TargetPriceOrderIndexApi(host=self._limit_host_, _session=self.session)
        params = TargetPriceOrderQueryParams(
            count=count,
            state=state,
        ).dict(exclude_none=True)

        response = api.call(params=params)
        return TargetPriceOrderResponse.parse_raw(b=response.content)

    @property
    def _limit_host_(self):
        return LIMIT_ORDER_HOST if self.env == "stg" else DEV_LIMIT_ORDER_HOST
