from typing import Optional
from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.rails.models import RailsRestApi, RailsRestService
from cdc.qa.apis.rails.models.mobile_airtime import (
    MobileAirtimeTopupAmountRequestData,
    MobileAirtimeTopupAmountResponse,
    MobileAirtimeOrderCreateRequestData,
    MobileAirtimeOrderCreateResponse,
    MobileAirtimeQuotationCreateRequestData,
    MobileAirtimeQuotationCreateResponse,
    MobileAirtimePaymentCreateRequestData,
    MobileAirtimePaymentCreateResponse,
)


class MobileAirtimeTopupAmountApi(RailsRestApi):
    """Get Topup option by phone number"""

    path = "mobile_airtime/topup_amounts"
    method = HttpMethods.POST
    request_data_type = MobileAirtimeTopupAmountRequestData
    response_type = MobileAirtimeTopupAmountResponse


class MobileAirtimeOrderCreateApi(RailsRestApi):
    """Create mobile airtime order"""

    path = "mobile_airtime/orders/create"
    method = HttpMethods.POST
    request_data_type = MobileAirtimeOrderCreateRequestData
    response_type = MobileAirtimeOrderCreateResponse


class MobileAirtimeQuotationCreateApi(RailsRestApi):
    """Create mobile airtime quotation"""

    path = "mobile_airtime/payments/quotation/create"
    method = HttpMethods.POST
    request_data_type = MobileAirtimeQuotationCreateRequestData
    response_type = MobileAirtimeQuotationCreateResponse


class MobileAirtimePaymentCreateApi(RailsRestApi):
    """Create mobile airtime payment"""

    path = "mobile_airtime/payments/create"
    method = HttpMethods.POST
    request_data_type = MobileAirtimePaymentCreateRequestData
    response_type = MobileAirtimePaymentCreateResponse


class MobileAirtimeService(RailsRestService):
    def get_topup_amount(self, phone: str) -> MobileAirtimeTopupAmountResponse:
        api = MobileAirtimeTopupAmountApi(host=self.host, _session=self.session)
        data = MobileAirtimeTopupAmountRequestData(recipient_phone=phone).dict(exclude_none=True)

        response = api.call(data=data)
        return MobileAirtimeTopupAmountResponse.parse_raw(b=response.content)

    def create_order(
        self,
        phone: str,
        operator_id: int,
        operator_name: str,
        fx_rate: str,
        local_currency: str,
        local_amount: str,
        payment_currency: str,
        payment_amount: str,
        country_code: str,
    ) -> MobileAirtimeOrderCreateResponse:
        api = MobileAirtimeOrderCreateApi(host=self.host, _session=self.session)
        data = MobileAirtimeOrderCreateRequestData(
            recipient_phone=phone,
            operator_id=operator_id,
            operator_name=operator_name,
            fx_rate=fx_rate,
            local_currency=local_currency,
            local_amount=local_amount,
            payment_currency=payment_currency,
            payment_amount=payment_amount,
            country_code=country_code,
        ).dict(exclude_none=True)

        response = api.call(data=data)
        return MobileAirtimeOrderCreateResponse.parse_raw(b=response.content)

    def create_quotation(
        self, order_id: str, from_currency: str, otp: Optional[str]
    ) -> MobileAirtimeQuotationCreateResponse:
        api = MobileAirtimeQuotationCreateApi(host=self.host, _session=self.session)
        data = MobileAirtimeQuotationCreateRequestData(
            order_id=order_id,
            from_currency=from_currency,
            otp=otp,
        ).dict()

        response = api.call(data=data)
        return MobileAirtimeQuotationCreateResponse.parse_raw(b=response.content)

    def create_payment(self, quotation_id: str, order_id: str, passcode: str) -> MobileAirtimePaymentCreateResponse:
        api = MobileAirtimePaymentCreateApi(host=self.host, _session=self.session)
        data = MobileAirtimePaymentCreateRequestData(
            quotation_id=quotation_id,
            order_id=order_id,
            passcode=passcode,
        ).dict(exclude_none=True)

        response = api.call(data=data)
        return MobileAirtimePaymentCreateResponse.parse_raw(b=response.content)
