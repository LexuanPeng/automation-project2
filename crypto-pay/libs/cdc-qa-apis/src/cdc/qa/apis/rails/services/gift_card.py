from typing import Optional
from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.rails.models import RailsRestApi, RailsRestService
from cdc.qa.apis.rails.models.gift_card import (
    GiftCardBrandsQueryParams,
    GiftCardBrandsResponse,
    GiftCardOrderRequestData,
    GiftCardOrderResponse,
    GiftCardPaymentsQuotationRequestData,
    GiftCardPaymentsQuotationResponse,
    GiftCardPaymentsRequestData,
    GiftCardPaymentsResponse,
)


class GiftCardBrandsApi(RailsRestApi):
    """Get gift card brands"""

    path = "gift_card/brands"
    method = HttpMethods.GET
    request_params_type = GiftCardBrandsQueryParams
    response_type = GiftCardBrandsResponse


class GiftCardOrdersApi(RailsRestApi):
    """Create gift card order"""

    path = "gift_card/orders/create"
    method = HttpMethods.POST
    request_data_type = GiftCardOrderRequestData
    response_type = GiftCardOrderResponse


class GiftCardPaymentsQuotationApi(RailsRestApi):
    """Create gift card payment quotation"""

    path = "gift_card/payments/quotation/create"
    method = HttpMethods.POST
    request_data_type = GiftCardPaymentsQuotationRequestData
    response_type = GiftCardPaymentsQuotationResponse


class GiftCardPaymentsApi(RailsRestApi):
    """Create gift card payment"""

    path = "gift_card/payments/create"
    method = HttpMethods.POST
    request_data_type = GiftCardPaymentsRequestData
    response_type = GiftCardPaymentsResponse


class GiftCardService(RailsRestService):
    def get_gift_card_brands(self, country: str) -> GiftCardBrandsResponse:
        api = GiftCardBrandsApi(host=self.host, _session=self.session)
        params = GiftCardBrandsQueryParams(country=country).dict(exclude_none=True)

        response = api.call(params=params)
        return GiftCardBrandsResponse.parse_raw(b=response.content)

    def create_gift_card_order(
        self,
        currency: str,
        gift_card_id: str,
        price: float,
        country: str,
    ) -> GiftCardOrderResponse:
        api = GiftCardOrdersApi(host=self.host, _session=self.session)
        data = GiftCardOrderRequestData(
            currency=currency,
            gift_card_id=gift_card_id,
            price=price,
            country=country,
        ).dict(exclude_none=True)

        response = api.call(data=data)
        return GiftCardOrderResponse.parse_raw(b=response.content)

    def create_gift_card_quotation(
        self,
        from_currency: str,
        order_id: str,
        otp: Optional[str] = None,
    ) -> GiftCardPaymentsQuotationResponse:
        api = GiftCardPaymentsQuotationApi(host=self.host, _session=self.session)
        data = GiftCardPaymentsQuotationRequestData(
            from_currency=from_currency,
            order_id=order_id,
            otp=otp,
        ).dict(exclude_none=True)

        response = api.call(data=data)
        return GiftCardPaymentsQuotationResponse.parse_raw(response.content)

    def create_gift_card_payment(
        self,
        passcode: str,
        quotation_id: str,
        order_id: str,
    ) -> GiftCardPaymentsResponse:
        api = GiftCardPaymentsApi(host=self.host, _session=self.session)
        data = GiftCardPaymentsRequestData(
            passcode=passcode,
            quotation_id=quotation_id,
            order_id=order_id,
        ).dict(exclude_none=True)

        response = api.call(data=data)
        return GiftCardPaymentsResponse.parse_raw(response.content)
