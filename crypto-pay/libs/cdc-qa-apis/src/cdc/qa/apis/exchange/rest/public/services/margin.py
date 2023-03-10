from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.exchange.rest.rest_base import ExchangeRestApi, ExchangeRestService
from ..models.margin import GetTransferCurrenciesResponse, GetLoanCurrenciesResponse

"""
include API models:
public/margin/get-transfer-currencies
public/margin/get-loan-currencies
"""


class GetTransferCurrenciesApi(ExchangeRestApi):
    path = "public/margin/get-transfer-currencies"
    method = HttpMethods.GET
    response_type = GetTransferCurrenciesResponse


class GetLoanCurrenciesApi(ExchangeRestApi):
    path = "public/margin/get-loan-currencies"
    method = HttpMethods.GET
    response_type = GetLoanCurrenciesResponse


class MarginService(ExchangeRestService):
    def get_transfer_currencies(self) -> GetTransferCurrenciesResponse:
        api = GetTransferCurrenciesApi(host=self.host, _session=self.session)
        response = GetTransferCurrenciesResponse.parse_raw(b=api.call().content)
        return response

    def get_loan_currencies(self) -> GetLoanCurrenciesResponse:
        api = GetLoanCurrenciesApi(host=self.host, _session=self.session)
        response = GetLoanCurrenciesResponse.parse_raw(b=api.call().content)
        return response
