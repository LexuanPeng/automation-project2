from decimal import Decimal

from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.exchange.rest.rest_base import ExchangeRestApi, ExchangeRestService

from ..models.account import (
    CreateWithdrawalRequest,
    CreateWithdrawalRequestParams,
    CreateWithdrawalResponse,
    GetAccountSummaryRequestBody,
    GetAccountSummaryRequestParams,
    GetAccountSummaryResponse,
    GetDepositAddressRequest,
    GetDepositAddressRequestParams,
    GetDepositAddressResponse,
    GetDepositHistoryRequest,
    GetDepositHistoryRequestParams,
    GetDepositHistoryResponse,
    GetWithdrawalHistoryRequest,
    GetWithdrawalHistoryRequestParams,
    GetWithdrawalHistoryResponse,
    GetCurrencyNetworksRequest,
    GetCurrencyNetworksResponse,
)


class GetAccountSummaryApi(ExchangeRestApi):
    """exchange-private get the account balance of a user for a particular token"""

    path = "private/get-account-summary"
    method = HttpMethods.POST
    request_data_type = GetAccountSummaryRequestBody
    response_type = GetAccountSummaryResponse


class GetWithdrawalHistoryApi(ExchangeRestApi):
    """exchange-private get the withdrawal history"""

    path = "private/get-withdrawal-history"
    method = HttpMethods.POST
    request_data_type = GetWithdrawalHistoryRequest
    response_type = GetWithdrawalHistoryResponse


class GetDepositHistoryApi(ExchangeRestApi):
    """exchange-private get the deposit history"""

    path = "private/get-deposit-history"
    method = HttpMethods.POST
    request_data_type = GetDepositHistoryRequest
    response_type = GetDepositHistoryResponse


class GetDepositAddressApi(ExchangeRestApi):
    """exchange-private get the deposit address"""

    path = "private/get-deposit-address"
    method = HttpMethods.POST
    request_data_type = GetDepositAddressRequest
    response_type = GetDepositAddressResponse


class CreateWithdrawalApi(ExchangeRestApi):
    """exchange-private get the deposit address"""

    path = "private/create-withdrawal"
    method = HttpMethods.POST
    request_data_type = CreateWithdrawalRequest
    response_type = CreateWithdrawalResponse


class GetCurrencyNetworksApi(ExchangeRestApi):
    """exchange-private get the deposit address"""

    path = "private/get-currency-networks"
    method = HttpMethods.POST
    request_data_type = GetCurrencyNetworksRequest
    response_type = GetCurrencyNetworksResponse


class AccountService(ExchangeRestService):
    def get_account_summary(self, currency: str = None) -> GetAccountSummaryResponse:
        """request get account summary
        Args:
            currency (str, optional): Specific currency, e.g. CRO. Omit for 'all'

        Returns:
            response: GetAccountSummaryResponse
        """
        api = GetAccountSummaryApi(host=self.host, _session=self.session)
        payload = GetAccountSummaryRequestBody(
            params=GetAccountSummaryRequestParams(currency=currency),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = GetAccountSummaryResponse.parse_raw(b=api.call(data=payload).content)

        return response

    def get_withdrawal_history(
        self,
        currency: str = None,
        start_ts: int = None,
        end_ts: int = None,
        page_size: int = None,
        page: int = None,
        status: str = None,
    ) -> GetWithdrawalHistoryResponse:
        """get withdrawl history

        Args:
            currency (str, optional): currency. Defaults to None.
            start_ts (int, optional): start timestamp. Defaults to None.
            end_ts (int, optional): end timestamp. Defaults to None.
            page_size (int, optional): page size. Defaults to None.
            page (int, optional): page number 0-based. Defaults to None.
            status (str, optional): 0 - Pending
                        1 - Processing
                        2 - Rejected
                        3 - Payment In-progress
                        4 - Payment Failed
                        5 - Completed
                        6 - Cancelled. Defaults to None.

        Returns:
            GetWithdrawalHistoryResponse: withdraw list
        """
        api = GetWithdrawalHistoryApi(host=self.host, _session=self.session)
        payload = GetWithdrawalHistoryRequest(
            params=GetWithdrawalHistoryRequestParams(
                currency=currency,
                start_ts=start_ts,
                end_ts=end_ts,
                page_size=page_size,
                page=page,
                status=status,
            ),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = GetWithdrawalHistoryResponse.parse_raw(b=api.call(data=payload).content)

        return response

    def get_deposit_history(
        self,
        currency: str = None,
        start_ts: int = None,
        end_ts: int = None,
        page_size: int = None,
        page: int = None,
        status: str = None,
    ) -> GetDepositHistoryResponse:
        """get deposit history

        Args:
            currency (str, optional): currency. Defaults to None.
            start_ts (int, optional): start timestamp. Defaults to None.
            end_ts (int, optional): end timestamp. Defaults to None.
            page_size (int, optional): page size. Defaults to None.
            page (int, optional): page number 0-based. Defaults to None.
            status (str, optional):
                        0 - Not Arrived
                        1 - Arrived
                        2 - Failed
                        3 - Pending. Defaults to None.

        Returns:
            GetDepositHistoryResponse: deposit list
        """
        api = GetDepositHistoryApi(host=self.host, _session=self.session)
        payload = GetDepositHistoryRequest(
            params=GetDepositHistoryRequestParams(
                currency=currency,
                start_ts=start_ts,
                end_ts=end_ts,
                page_size=page_size,
                page=page,
                status=status,
            ),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = GetDepositHistoryResponse.parse_raw(b=api.call(data=payload).content)

        return response

    def get_deposit_address(self, currency: str = None) -> GetDepositAddressResponse:
        """get deposit address

        Args:
            currency (str): currency name, Defaults to None.

        Returns:
            GetDepositAddressResponse: address response
        """
        api = GetDepositAddressApi(host=self.host, _session=self.session)
        payload = GetDepositAddressRequest(
            params=GetDepositAddressRequestParams(currency=currency),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = GetDepositAddressResponse.parse_raw(b=api.call(data=payload).content)

        return response

    def create_withdrawal(
        self, currency: str, amount: Decimal, address: str, client_wid: str = None, address_tag: str = None
    ) -> CreateWithdrawalResponse:
        """create withdrawal

        Args:
            currency (str): currency name
            amount (Decimal): withdrawal amount
            address (str): address
            client_wid (str, optional): client withdrawal id. Defaults to None.
            address_tag (str, optional): address identifier. Defaults to None.

        Returns:
            CreateWithdrawalResponse: create withdrawal response
        """
        api = CreateWithdrawalApi(host=self.host, _session=self.session)
        payload = CreateWithdrawalRequest(
            params=CreateWithdrawalRequestParams(
                client_wid=client_wid,
                currency=currency,
                amount=amount,
                address=address,
                address_tag=address_tag,
            ),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = CreateWithdrawalResponse.parse_raw(b=api.call(data=payload).content)

        return response

    def get_currency_networks(self) -> GetCurrencyNetworksResponse:
        """get currency networks

        Returns:
            GetCurrencyNetworksResponse: get currency networks response
        """
        api = GetCurrencyNetworksApi(host=self.host, _session=self.session)
        payload = GetCurrencyNetworksRequest(api_key=self.api_key, secret_key=self.secret_key).json(exclude_none=True)
        response = GetCurrencyNetworksResponse.parse_raw(b=api.call(data=payload).content)

        return response
