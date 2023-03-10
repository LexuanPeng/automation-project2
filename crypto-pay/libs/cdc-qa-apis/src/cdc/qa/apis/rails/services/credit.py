import logging

from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.rails.models import RailsRestService, RailsRestApi
from cdc.qa.apis.rails.models.credit import (
    CryptoCreditTermsResponse,
    CryptoCreditProgramOrderRequestData,
    CryptoCreditProgramOrderResponse,
    CryptoCreditProgramRequestData,
    CryptoCreditProgramResponse,
    CryptoCreditAccountShowResponse,
    CryptoCreditRePaymentOrderRequestData,
    CryptoCreditRePaymentOrderResponse,
    CryptoCreditRePaymentCreateRequestData,
    CryptoCreditRePaymentCreateResponse,
    CryptoCreditTransactionResponse,
)

logger = logging.getLogger(__name__)


class CryptoCreditTermsApi(RailsRestApi):
    """Get list of crypto credit terms when user enter Credit Home screen"""

    path = "crypto_credit/terms"
    method = HttpMethods.GET
    response_type = CryptoCreditTermsResponse


class CryptoCreditProgramOrderApi(RailsRestApi):
    """Create an order for credit program"""

    path = "crypto_credit/program/orders/create"
    method = HttpMethods.POST
    request_data_type = CryptoCreditProgramOrderRequestData
    response_type = CryptoCreditProgramOrderResponse


class CryptoCreditProgramApi(RailsRestApi):
    """Create a credit program"""

    path = "crypto_credit/programs/create"
    method = HttpMethods.POST
    request_data_type = CryptoCreditProgramRequestData
    response_type = CryptoCreditProgramResponse


class CryptoCreditAccountShowApi(RailsRestApi):
    """Show credit program account"""

    path = "crypto_credit/account/show"
    method = HttpMethods.GET
    response_type = CryptoCreditAccountShowResponse


class CryptoCreditRePaymentOrderApi(RailsRestApi):
    """Crypto Credit RePayment Create Order Api"""

    path = "crypto_credit/repayment/orders/create"
    method = HttpMethods.POST
    request_data_type = CryptoCreditRePaymentOrderRequestData
    response_type = CryptoCreditRePaymentOrderResponse


class CryptoCreditRePaymentCreateApi(RailsRestApi):
    """Crypto Credit RePayment Create Api"""

    path = "crypto_credit/repayments/create"
    method = HttpMethods.POST
    request_data_type = CryptoCreditRePaymentCreateRequestData
    response_type = CryptoCreditRePaymentCreateResponse


class CryptoCreditTransactionApi(RailsRestApi):
    """CryptoCreditTransactionApi"""

    path = "crypto_credit/transactions"
    method = HttpMethods.GET
    response_type = CryptoCreditTransactionResponse


class CreditService(RailsRestService):
    def _crypto_credit_terms(self) -> CryptoCreditTermsResponse:
        api = CryptoCreditTermsApi(host=self.host, _session=self.session)

        response = api.call()
        return CryptoCreditTermsResponse.parse_raw(b=response.content)

    def _crypto_credit_program_order_create(
        self, loan_amount: str, payment_type: str, term_id: str, loan_currency: str, payment_currency: str
    ) -> CryptoCreditProgramOrderResponse:
        api = CryptoCreditProgramOrderApi(host=self.host, _session=self.session)
        data = CryptoCreditProgramOrderRequestData(
            loan_amount=loan_amount,
            payment_type=payment_type,
            term_id=term_id,
            loan_currency=loan_currency,
            payment_currency=payment_currency,
        ).dict(exclude_none=True)

        response = api.call(data=data)
        return CryptoCreditProgramOrderResponse.parse_raw(b=response.content)

    def _crypto_credit_program_create(self, order_id: str, passcode: str) -> CryptoCreditProgramResponse:
        api = CryptoCreditProgramApi(host=self.host, _session=self.session)
        data = CryptoCreditProgramRequestData(order_id=order_id, passcode=passcode).dict(exclude_none=True)

        response = api.call(data=data)
        return CryptoCreditProgramResponse.parse_raw(b=response.content)

    def create_crypto_credit_program(self, passcode: str, loan_amount: str, loan_currency: str, payment_currency: str):
        credit_terms = next(
            filter(
                lambda x: x.collateral_currency.upper() == payment_currency.upper(),
                self._crypto_credit_terms().crypto_credit_terms,
            )
        )
        order_id = self._crypto_credit_program_order_create(
            loan_amount=loan_amount,
            payment_type="crypto_wallet",
            term_id=credit_terms.id,
            loan_currency=loan_currency,
            payment_currency=payment_currency,
        ).crypto_credit_program_order.id

        id = self._crypto_credit_program_create(order_id=order_id, passcode=passcode).crypto_credit_program.id
        logger.debug(f"Crypto credit program created: id={id}")

    def crypto_credit_account_show(self) -> CryptoCreditAccountShowResponse:
        api = CryptoCreditAccountShowApi(host=self.host, _session=self.session)

        response = api.call()
        return CryptoCreditAccountShowResponse.parse_raw(b=response.content)

    def repayment_order_create(
        self,
        payment_type: str,
        currency: str,
        amount: str,
        program_id: str,
        payment_currency: str,
    ) -> CryptoCreditRePaymentOrderResponse:
        api = CryptoCreditRePaymentOrderApi(host=self.host, _session=self.session)
        data = CryptoCreditRePaymentOrderRequestData(
            payment_type=payment_type,
            currency=currency,
            amount=amount,
            program_id=program_id,
            payment_currency=payment_currency,
        ).dict(exclude_none=True)

        response = api.call(data=data)
        return CryptoCreditRePaymentOrderResponse.parse_raw(b=response.content)

    def repayment_create(self, order_id: str, passcode: str) -> CryptoCreditRePaymentCreateResponse:
        api = CryptoCreditRePaymentCreateApi(host=self.host, _session=self.session)
        data = CryptoCreditRePaymentCreateRequestData(order_id=order_id, passcode=passcode).dict(exclude_none=True)

        response = api.call(data=data)
        return CryptoCreditRePaymentCreateResponse.parse_raw(b=response.content)

    def crypto_credit_transactions(self) -> CryptoCreditTransactionResponse:
        api = CryptoCreditTransactionApi(host=self.host, _session=self.session)

        response = api.call()
        return CryptoCreditTransactionResponse.parse_raw(b=response.content)
