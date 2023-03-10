import uuid
from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.crypto_pay.models import PayRestApi, payment, PayServerService, BearerPKAuth


class CreatePaymentApi(PayRestApi):
    path = "payments"
    method = HttpMethods.POST
    request_data_type = payment.CreatePaymentRequestData
    response_type = payment.CreatePaymentResponse


class PaymentService(PayServerService):
    def create_payment(
        self,
        pk_key: str,
        currency: str,
        amount: str,
        description: str = f"Automation Test {str(uuid.uuid4())}",
        order_id: str = f"Automation {str(uuid.uuid4())}",
        delayed_capture: str = "false",
    ) -> payment.CreatePaymentResponse:
        api = CreatePaymentApi(host=self.host, _session=self.session)
        data = payment.CreatePaymentRequestData(
            currency=currency,
            amount=amount,
            description=description,
            order_id=order_id,
            delayed_capture=delayed_capture,
            meta_data=payment.MetaData().dict(),
        ).dict(exclude_none=True)

        auth = BearerPKAuth(pk_key)
        response = api.call(auth=auth, json=data)
        return payment.CreatePaymentResponse.parse_raw(b=response.content)

    def create_sub_merchant_payment(
        self,
        pk_key: str,
        currency: str,
        amount: str,
        sub_merchant_id: str,
        description: str = f"Automation Test {str(uuid.uuid4())}",
        order_id: str = f"Automation {str(uuid.uuid4())}",
        delayed_capture: str = "false",
    ) -> payment.CreatePaymentResponse:
        api = CreatePaymentApi(host=self.host, _session=self.session)
        data = payment.CreatePaymentRequestData(
            currency=currency,
            amount=amount,
            description=description,
            order_id=order_id,
            delayed_capture=delayed_capture,
            meta_data=payment.MetaData().dict(),
            sub_merchant_id=sub_merchant_id,
        ).dict(exclude_none=True)

        auth = BearerPKAuth(pk_key)
        response = api.call(auth=auth, json=data)
        return payment.CreatePaymentResponse.parse_raw(b=response.content)
