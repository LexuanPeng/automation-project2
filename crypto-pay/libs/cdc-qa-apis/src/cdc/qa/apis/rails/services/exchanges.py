import logging

from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.rails.models import RailsRestService, RailsRestApi
from cdc.qa.apis.rails.models.exchanges import (
    ExchangesQuotationCreateRequestData,
    ExchangesQuotationCreateResponse,
    ExchangesCreateRequestData,
    ExchangesCreateResponse,
    TransferFundToExchangeRequestData,
    TransferFundToExchangeResponse,
)

logger = logging.getLogger(__name__)


class ExchangesQuotationCreateApi(RailsRestApi):
    """Create an exchange quotation"""

    path = "exchanges/quotation/create"
    method = HttpMethods.POST
    request_data_type = ExchangesQuotationCreateRequestData
    response_type = ExchangesQuotationCreateResponse


class ExchangesCreateApi(RailsRestApi):
    """Create an exchange transaction"""

    path = "exchanges/create"
    method = HttpMethods.POST
    request_data_type = ExchangesCreateRequestData
    response_type = ExchangesCreateResponse


class TransferFundToExchangeApi(RailsRestApi):
    """TransferFundToExchangeApi"""

    path = "ex/deposits/create"
    method = HttpMethods.POST
    request_data_type = TransferFundToExchangeRequestData
    response_type = TransferFundToExchangeResponse


class ExchangesService(RailsRestService):
    def _exchanges_quotation_create(
        self, side: str, from_currency: str, to_currency: str, to_amount: str = None, from_amount: str = None
    ) -> ExchangesQuotationCreateResponse:
        api = ExchangesQuotationCreateApi(host=self.host, _session=self.session)
        params = {
            "side": side,
            "to_amount": to_amount,
            "from_amount": from_amount,
            "from": from_currency,
            "to": to_currency,
        }
        params = dict(filter(lambda item: item[1] is not None, params.items()))
        payload = ExchangesQuotationCreateRequestData(**params).dict(exclude_none=True, by_alias=True)

        response = api.call(data=payload)
        return ExchangesQuotationCreateResponse.parse_raw(b=response.content)

    def _exchanges_create(self, side: str, quotation_id: str, passcode: str) -> ExchangesCreateResponse:
        api = ExchangesCreateApi(host=self.host, _session=self.session)
        data = ExchangesCreateRequestData(side=side, quotation_id=quotation_id, passcode=passcode).dict(
            exclude_none=True
        )

        response = api.call(data=data)
        return ExchangesCreateResponse.parse_raw(b=response.content)

    def buy_crypto_with_crypto(self, passcode: str, to_amount: str, from_currency: str, to_currency: str):
        """Buy crypto with crypto"""
        quotation_id = self._exchanges_quotation_create(
            side="buy", to_amount=to_amount, from_currency=from_currency, to_currency=to_currency
        ).quotation.id
        exchanges_transaction = self._exchanges_create(
            side="buy", quotation_id=quotation_id, passcode=passcode
        ).transaction

        logger.debug(
            f"Buy crypto with crypto {exchanges_transaction.description} "
            f"successfully: {exchanges_transaction.rate_desc}"
        )

    def transfer_fund_to_exchange(self, currency: str, amount: str, passcode: str) -> TransferFundToExchangeResponse:
        api = TransferFundToExchangeApi(host=self.host, _session=self.session)
        data = TransferFundToExchangeRequestData(
            currency=currency,
            amount=amount,
            passcode=passcode,
        ).dict(exclude_none=True)

        response = api.call(data=data)
        return TransferFundToExchangeResponse.parse_raw(b=response.content)
