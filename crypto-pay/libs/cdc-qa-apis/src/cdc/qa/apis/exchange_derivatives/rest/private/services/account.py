from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.exchange_derivatives.rest.rest_base import DerivativesRestApi, DerivativesRestService

from ..models.account import (
    ChangeAccountLeverageRequestBody,
    ChangeAccountLeverageRequestParams,
    ChangeAccountLeverageResponse,
    GetAccountInfoRequestBody,
    GetAccountInfoResponse,
    GetSubAccountBalancesRequestBody,
    GetSubAccountBalancesResponse,
    UserBalanceRequestBody,
    UserBalanceResponse,
)


class UserBalanceApi(DerivativesRestApi):
    """exchange deriv private get User Balance. Returns the account balance of a user"""

    path = "private/user-balance"
    method = HttpMethods.POST
    request_data_type = UserBalanceRequestBody
    response_type = UserBalanceResponse


class GetSubAccountBalancesApi(DerivativesRestApi):
    """exchange deriv private get Get SubAccount Balances. Returns the sub account balance of a user"""

    path = "private/get-subaccount-balances"
    method = HttpMethods.POST
    request_data_type = GetSubAccountBalancesRequestBody
    response_type = GetSubAccountBalancesResponse


class ChangeAccountLeverageApi(DerivativesRestApi):
    """exchange-private deriv change account leverage"""

    path = "private/change-account-leverage"
    method = HttpMethods.POST
    request_data_type = ChangeAccountLeverageRequestBody
    response_type = ChangeAccountLeverageResponse


class GetAccountInfoApi(DerivativesRestApi):
    """exchange-private deriv get account info"""

    path = "private/get-account-info"
    method = HttpMethods.POST
    request_data_type = GetAccountInfoRequestBody
    response_type = GetAccountInfoResponse


class AccountService(DerivativesRestService):
    def user_balance(self) -> UserBalanceResponse:
        """request get user-balance

        Returns:
            response: UserBalanceResponse
        """
        api = UserBalanceApi(host=self.host, _session=self.session)
        payload = UserBalanceRequestBody(
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = UserBalanceResponse.parse_raw(b=api.call(data=payload).content)
        return response

    def get_subaccount_balances(self) -> GetSubAccountBalancesResponse:
        """request get-subaccount-balances

        Returns:
            response: GetSubAccountBalancesResponse
        """
        api = GetSubAccountBalancesApi(host=self.host, _session=self.session)
        payload = GetSubAccountBalancesRequestBody(
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = GetSubAccountBalancesResponse.parse_raw(b=api.call(data=payload).content)
        return response

    def change_account_leverage(self, account_id: str, leverage: int) -> ChangeAccountLeverageResponse:
        """request change-account-leverage
        Args:
            account_id (str): account ID to change the leverage.
            leverage (int): maximum leverage to be used for the account. Valid values are between 1-100 (inclusive).
        Returns:
            response: ChangeAccountLeverageResponse
        """
        api = ChangeAccountLeverageApi(host=self.host, _session=self.session)
        payload = ChangeAccountLeverageRequestBody(
            params=ChangeAccountLeverageRequestParams(account_id=account_id, leverage=leverage),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = ChangeAccountLeverageResponse.parse_raw(b=api.call(data=payload).content)

        return response

    def get_account_info(self) -> GetAccountInfoResponse:
        """request get-account-info

        Returns:
            response: GetAccountInfoResponse
        """
        api = GetAccountInfoApi(host=self.host, _session=self.session)
        payload = GetAccountInfoRequestBody(
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = GetAccountInfoResponse.parse_raw(b=api.call(data=payload).content)

        return response
