import logging

from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.rails.models import RailsRestService, RailsRestApi
from cdc.qa.apis.rails.models.earn import (
    CryptoEarnTermsResponse,
    CryptoEarnProgramOrderRequestData,
    CryptoEarnProgramOrderResponse,
    CryptoEarnProgramRequestData,
    CryptoEarnProgramResponse,
    CryptoEarnProgramsResponse,
    CryptoEarnWithdrawalsCreateRequestData,
    CryptoEarnWithdrawalsCreateResponse,
)

logger = logging.getLogger(__name__)


class CryptoEarnTermsApi(RailsRestApi):
    """Get list of crypto earn terms when user enter Earn Home screen"""

    path = "crypto_earn/terms"
    method = HttpMethods.GET
    response_type = CryptoEarnTermsResponse


class CryptoEarnProgramOrderApi(RailsRestApi):
    """Create an order for earn program"""

    path = "crypto_earn/programs/orders/create"
    method = HttpMethods.POST
    request_data_type = CryptoEarnProgramOrderRequestData
    response_type = CryptoEarnProgramOrderResponse


class CryptoEarnProgramApi(RailsRestApi):
    """Create a earn program"""

    path = "crypto_earn/programs/create"
    method = HttpMethods.POST
    request_data_type = CryptoEarnProgramRequestData
    response_type = CryptoEarnProgramResponse


class CryptoEarnProgramsApi(RailsRestApi):
    """Get user earn earn programs"""

    path = "crypto_earn/programs"
    method = HttpMethods.GET
    response_type = CryptoEarnProgramsResponse


class CryptoEarnWithdrawalsCreateApi(RailsRestApi):
    """Create an earn withdrawal"""

    path = "crypto_earn/withdrawals/create"
    method = HttpMethods.POST
    request_data_type = CryptoEarnWithdrawalsCreateRequestData
    response_type = CryptoEarnWithdrawalsCreateResponse


class EarnService(RailsRestService):
    def _crypto_earn_terms(self) -> CryptoEarnTermsResponse:
        api = CryptoEarnTermsApi(host=self.host, _session=self.session)

        response = api.call()
        return CryptoEarnTermsResponse.parse_raw(b=response.content)

    def _crypto_earn_program_order_create(
        self, deposit_amount: str, payment_type: str, term_id: str, deposit_currency: str, program_currency: str
    ) -> CryptoEarnProgramOrderResponse:
        api = CryptoEarnProgramOrderApi(host=self.host, _session=self.session)
        data = CryptoEarnProgramOrderRequestData(
            deposit_amount=deposit_amount,
            payment_type=payment_type,
            crypto_earn_term_id=term_id,
            deposit_currency=deposit_currency,
            program_currency=program_currency,
        ).dict(exclude_none=True)

        response = api.call(data=data)
        return CryptoEarnProgramOrderResponse.parse_raw(b=response.content)

    def _crypto_earn_program_create(
        self, order_id: str, passcode: str, term_id: str, payment_type: str, payment_currency: str
    ) -> CryptoEarnProgramResponse:
        api = CryptoEarnProgramApi(host=self.host, _session=self.session)
        data = CryptoEarnProgramRequestData(
            crypto_earn_program_order_id=order_id,
            passcode=passcode,
            crypto_earn_term_id=term_id,
            payment_type=payment_type,
            payment_currency=payment_currency,
        ).dict(exclude_none=True)

        response = api.call(data=data)
        return CryptoEarnProgramResponse.parse_raw(b=response.content)

    def crypto_earn_programs_index(self) -> CryptoEarnProgramsResponse:
        api = CryptoEarnProgramsApi(host=self.host, _session=self.session)

        response = api.call()
        return CryptoEarnProgramsResponse.parse_raw(b=response.content)

    def crypto_earn_withdrawal_create(self, passcode: str, program_id: str, currency: str, amount: str):
        api = CryptoEarnWithdrawalsCreateApi(host=self.host, _session=self.session)
        data = CryptoEarnWithdrawalsCreateRequestData(
            passcode=passcode,
            amount=amount,
            currency=currency,
            crypto_earn_program_id=program_id,
        ).dict(exclude_none=True)

        response = api.call(data=data)
        return CryptoEarnWithdrawalsCreateResponse.parse_raw(b=response.content)

    def create_crypto_earn_program(
        self,
        passcode: str,
        deposit_amount: str,
        deposit_currency: str,
        program_currency: str,
        program_name: str,
        payment_type: str = "crypto_wallet",
    ):
        earn_term = next(filter(lambda x: x.name == program_name, self._crypto_earn_terms().crypto_earn_terms))
        order_id = self._crypto_earn_program_order_create(
            deposit_amount=deposit_amount,
            payment_type=payment_type,
            term_id=earn_term.id,
            deposit_currency=deposit_currency,
            program_currency=program_currency,
        ).crypto_earn_deposit_order.id

        id = self._crypto_earn_program_create(
            order_id=order_id,
            passcode=passcode,
            term_id=earn_term.id,
            payment_type=payment_type,
            payment_currency=deposit_currency,
        ).crypto_earn_program.id
        logger.debug(f"Crypto earn program created: id={id}")
