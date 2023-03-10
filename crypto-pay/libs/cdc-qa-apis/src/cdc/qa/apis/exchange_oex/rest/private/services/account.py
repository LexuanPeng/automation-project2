from decimal import Decimal
from typing import List

from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.exchange_oex.models import ExchangeRequestParams
from cdc.qa.apis.exchange_oex.rest.rest_base import ExchangeRestApi, ExchangeRestService

from ..models.account import (
    ChangeAccountLeverageRequestBody,
    ChangeAccountLeverageRequestParams,
    ChangeAccountLeverageResponse,
    CreateIntraTransferRequestBody,
    CreateIntraTransferRequestParams,
    CreateIntraTransferResponse,
    CreateSubaccountMultiTransferRequest,
    CreateSubaccountMultiTransferRequestParams,
    CreateSubaccountMultiTransferResponse,
    CreateSubaccountTransferRequest,
    CreateSubaccountTransferRequestParams,
    CreateSubaccountTransferResponse,
    CreateWithdrawalRequest,
    CreateWithdrawalRequestParams,
    CreateWithdrawalResponse,
    GetAccountInfoRequestBody,
    GetAccountInfoResponse,
    GetAccountRequestBody,
    GetAccountResponse,
    GetCurrencyNetworksRequest,
    GetCurrencyNetworksResponse,
    GetDepositAddressRequest,
    GetDepositAddressRequestParams,
    GetDepositAddressResponse,
    GetRiskInfoRequestBody,
    GetRiskInfoRequestParams,
    GetRiskInfoResponse,
    GetSubAccountBalancesRequestBody,
    GetSubAccountBalancesResponse,
    UserBalanceHistoryRequestBody,
    UserBalanceHistoryRequestParams,
    UserBalanceHistoryResponse,
    UserBalanceRequestBody,
    UserBalanceResponse,
)


class CreateWithdrawalApi(ExchangeRestApi):
    """exchange-private get the deposit address"""

    path = "private/create-withdrawal"
    method = HttpMethods.POST
    request_data_type = CreateWithdrawalRequest
    response_type = CreateWithdrawalResponse


class ChangeAccountLeverageApi(ExchangeRestApi):
    """exchange-private deriv change account leverage"""

    path = "private/change-account-leverage"
    method = HttpMethods.POST
    request_data_type = ChangeAccountLeverageRequestBody
    response_type = ChangeAccountLeverageResponse


class GetCurrencyNetworksApi(ExchangeRestApi):
    """exchange-private get the deposit address"""

    path = "private/get-currency-networks"
    method = HttpMethods.POST
    request_data_type = GetCurrencyNetworksRequest
    response_type = GetCurrencyNetworksResponse


class GetSubAccountBalancesApi(ExchangeRestApi):
    """exchange deriv private get Get SubAccount Balances. Returns the sub account balance of a user"""

    path = "private/get-subaccount-balances"
    method = HttpMethods.POST
    request_data_type = GetSubAccountBalancesRequestBody
    response_type = GetSubAccountBalancesResponse


class UserBalanceApi(ExchangeRestApi):
    """exchange deriv private get User Balance. Returns the account balance of a user"""

    path = "private/user-balance"
    method = HttpMethods.POST
    request_data_type = UserBalanceRequestBody
    response_type = UserBalanceResponse


class GetDepositAddressApi(ExchangeRestApi):
    """exchange-private get the deposit address"""

    path = "private/get-deposit-address"
    method = HttpMethods.POST
    request_data_type = GetDepositAddressRequest
    response_type = GetDepositAddressResponse


class CreateSubaccountTransferApi(ExchangeRestApi):
    """exchange-private create a sub account transfer"""

    path = "private/create-subaccount-transfer"
    method = HttpMethods.POST
    request_data_type = CreateSubaccountTransferRequest
    response_type = CreateSubaccountTransferResponse


class CreateSubaccountMultiTransferApi(ExchangeRestApi):
    """exchange-private create a sub account mutil transfer"""

    path = "private/create-subaccount-multi-transfer"
    method = HttpMethods.POST
    request_data_type = CreateSubaccountMultiTransferRequest
    response_type = CreateSubaccountMultiTransferResponse


class UserBalanceHistoryApi(ExchangeRestApi):
    """exchange-private get user balance history"""

    path = "private/user-balance-history"
    method = HttpMethods.POST
    request_data_type = UserBalanceHistoryRequestBody
    response_type = UserBalanceHistoryResponse


class GetAccountsApi(ExchangeRestApi):
    """exchange-private get accounts"""

    path = "private/get-accounts"
    method = HttpMethods.POST
    request_data_type = GetAccountRequestBody
    response_type = GetAccountResponse


class GetAccountInfoApi(ExchangeRestApi):
    """exchange-private get account info"""

    path = "private/get-account-info"
    method = HttpMethods.POST
    request_data_type = GetAccountInfoRequestBody
    response_type = GetAccountInfoResponse


class GetRiskInfoApi(ExchangeRestApi):
    """exchange private get risk info"""

    path = "private/get-risk-info"
    method = HttpMethods.POST
    request_data_type = GetRiskInfoRequestBody
    response_type = GetRiskInfoResponse


class CreateIntraTransferApi(ExchangeRestApi):
    """exchange private create-intra-transfer"""

    path = "private/create-intra-transfer"
    method = HttpMethods.POST
    request_data_type = CreateIntraTransferRequestBody
    response_type = CreateIntraTransferResponse


class AccountService(ExchangeRestService):
    def user_balance(self, system_label: str = None) -> UserBalanceResponse:
        """request get user-balance

        Returns:
            response: UserBalanceResponse
        """
        api = UserBalanceApi(host=self.host, _session=self.session)
        payload = UserBalanceRequestBody(
            api_key=self.api_key,
            secret_key=self.secret_key,
            params=ExchangeRequestParams(system_label=system_label),
        ).json(exclude_none=True)
        response = UserBalanceResponse.parse_raw(b=api.call(data=payload).content)
        return response

    def get_subaccount_balances(self, system_label: str = None) -> GetSubAccountBalancesResponse:
        """request get-subaccount-balances

        Returns:
            response: GetSubAccountBalancesResponse
        """
        api = GetSubAccountBalancesApi(host=self.host, _session=self.session)
        payload = GetSubAccountBalancesRequestBody(
            api_key=self.api_key, secret_key=self.secret_key, params=ExchangeRequestParams(system_label=system_label)
        ).json(exclude_none=True)
        response = GetSubAccountBalancesResponse.parse_raw(b=api.call(data=payload).content)
        return response

    def user_balance_history(
        self,
        timeframe=None,
        end_time=None,
        limit=None,
        system_label: str = None,
    ) -> UserBalanceHistoryResponse:
        """request get-user-balances-history

        Returns:
            response: UserBalanceHistoryResponse
        """
        api = UserBalanceHistoryApi(host=self.host, _session=self.session)
        payload = UserBalanceHistoryRequestBody(
            params=UserBalanceHistoryRequestParams(
                timeframe=timeframe,
                end_time=end_time,
                limit=limit,
                system_label=system_label,
            ),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = UserBalanceHistoryResponse.parse_raw(b=api.call(data=payload).content)
        return response

    def change_account_leverage(
        self,
        account_id: str,
        leverage: int,
        system_label: str = None,
    ) -> ChangeAccountLeverageResponse:
        """request change-account-leverage
        Args:
            account_id (str): account ID to change the leverage.
            leverage (int): maximum leverage to be used for the account. Valid values are between 1-100 (inclusive).
        Returns:
            response: ChangeAccountLeverageResponse
        """
        api = ChangeAccountLeverageApi(host=self.host, _session=self.session)
        payload = ChangeAccountLeverageRequestBody(
            params=ChangeAccountLeverageRequestParams(
                account_id=account_id,
                leverage=leverage,
                system_label=system_label,
            ),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = ChangeAccountLeverageResponse.parse_raw(b=api.call(data=payload).content)

        return response

    def get_account_info(self, system_label: str = None) -> GetAccountInfoResponse:
        """request get-account-info

        Returns:
            response: GetAccountInfoResponse
        """
        api = GetAccountInfoApi(host=self.host, _session=self.session)
        payload = GetAccountInfoRequestBody(
            api_key=self.api_key,
            secret_key=self.secret_key,
            params=ExchangeRequestParams(system_label=system_label),
        ).json(exclude_none=True)
        response = GetAccountInfoResponse.parse_raw(b=api.call(data=payload).content)

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

    def create_subaccount_transfer(
        self, from_side: str, to: str, currency: str, amount: str, system_label: str = None
    ) -> CreateSubaccountTransferResponse:
        """create subaccount transfer

        Args:
            from_side (str): from side account id
            to (str): to side account id
            currency (str): currency name
            amount (str): The amount to be transferred

        Returns:
            CreateSubaccountTransferResponse: response
        """
        api = CreateSubaccountTransferApi(host=self.host, _session=self.session)
        params = {
            "system_label": system_label,
            "from": from_side,
            "to": to,
            "currency": currency,
            "amount": amount,
        }
        payload = CreateSubaccountTransferRequest(
            params=CreateSubaccountTransferRequestParams(**params),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True, by_alias=True)
        response = CreateSubaccountTransferResponse.parse_raw(b=api.call(data=payload).content)

        return response

    def create_intra_transfer(
        self, to: str, currency: str, amount: str, system_label: str = None
    ) -> CreateIntraTransferResponse:
        """create intra transfer

        Args:
            to (str): to side account id
            currency (str): currency name
            amount (str): The amount to be transferred

        Returns:
            CreateIntraTransferResponse: response
        """
        api = CreateIntraTransferApi(host=self.host, _session=self.session)

        payload = CreateIntraTransferRequestBody(
            params=CreateIntraTransferRequestParams(
                system_label=system_label,
                to=to,
                currency=currency,
                amount=amount,
            ),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True, by_alias=True)
        response = CreateIntraTransferResponse.parse_raw(b=api.call(data=payload).content)

        return response

    def create_subaccount_multi_transfer(
        self, currencies: List[str], from_side: List[str], to: str, system_label: str = None
    ) -> CreateSubaccountMultiTransferResponse:
        """create subaccount multi transfer

        Args:
            from_side (list[str]): from side account id
            to (list[str]): to side account id
            currencies (str): currency name
            system_label (str): system label

        Returns:
            CreateSubaccountMultiTransferResponse: response
        """
        api = CreateSubaccountMultiTransferApi(host=self.host, _session=self.session)
        params = {
            "currencies": currencies,
            "from": from_side,
            "to": to,
            "system_label": system_label,
        }
        payload = CreateSubaccountMultiTransferRequest(
            params=CreateSubaccountMultiTransferRequestParams(**params),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True, by_alias=True)
        response = CreateSubaccountMultiTransferResponse.parse_raw(b=api.call(data=payload).content)

        return response

    def get_accounts(self) -> GetAccountResponse:
        """get accounts

        Returns:
            GetAccountResponse: response
        """
        api = GetAccountsApi(host=self.host, _session=self.session)
        payload = GetAccountRequestBody(
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = GetAccountResponse.parse_raw(b=api.call(data=payload).content)

        return response

    def get_risk_info(self, instrument_name: str) -> GetRiskInfoResponse:
        """
        request get risk info
        Args:
            instrument_name:

        Returns:

        """
        api = GetRiskInfoApi(host=self.host, _session=self.session)
        payload = GetRiskInfoRequestBody(
            params=GetRiskInfoRequestParams(instrument_name=instrument_name),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = GetRiskInfoResponse.parse_raw(b=api.call(data=payload).content)
        return response
