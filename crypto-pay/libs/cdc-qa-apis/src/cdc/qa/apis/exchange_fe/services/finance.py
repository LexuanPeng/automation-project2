from cdc.qa.apis.common.models.rest_api import HttpMethods

from ..fe_base import FeExchangeApi, FeExchangeRestService
from ..models.finance import (
    AccountBalanceResponse,
    AddStakingRequest,
    AddStakingRequestPath,
    AddStakingResponse,
    FeeRatesResponse,
    GetChargeAddressRequest,
    GetChargeAddressResponse,
    RemoveStakingRequest,
    RemoveStakingResponse,
    DoWithdrawRequest,
    DoWithdrawResponse,
    GetDepositWithdrawalHistoryResponse,
    GetDepositWithdrawalHistoryRequest,
)


class AddStakingApi(FeExchangeApi):
    path = "finance/add_staking"
    method = HttpMethods.POST
    request_data_type = AddStakingRequest
    response_type = AddStakingResponse


class RemoveStakingApi(FeExchangeApi):
    path = "finance/remove_staking"
    method = HttpMethods.POST
    request_data_type = RemoveStakingRequest
    response_type = RemoveStakingResponse


class FeeRatesApi(FeExchangeApi):
    path = "finance/fee_rates"
    method = HttpMethods.GET
    response_type = FeeRatesResponse


class GetChargeAddressApi(FeExchangeApi):
    path = "finance/get_charge_address"
    method = HttpMethods.POST
    request_data_type = GetChargeAddressRequest
    response_type = GetChargeAddressResponse


class V5AccountBalanceApi(FeExchangeApi):
    path = "finance/v5/account_balance"
    method = HttpMethods.GET
    response_type = AccountBalanceResponse


class DoWithdrawApi(FeExchangeApi):
    path = "finance/do_withdraw"
    method = HttpMethods.POST
    request_data_type = DoWithdrawRequest
    response_type = DoWithdrawResponse


class GetDepositWithdrawalHistoryApi(FeExchangeApi):
    path = "get-deposit-withdrawal-history"
    method = HttpMethods.GET
    request_params_type: GetDepositWithdrawalHistoryRequest
    response_type = GetDepositWithdrawalHistoryResponse


class FinanceService(FeExchangeRestService):
    def add_staking(self, symbol: str, add_amount: int, total_amount: int) -> AddStakingResponse:
        """
        Add Staking finance/add_staking
        :param symbol: e.g. "CRO"
        :param amount: e.g. 5000
        :return:
        """
        api = AddStakingApi(host=self.host, _session=self.session, exchange_token=self.exchange_token)
        path_params = AddStakingRequestPath(symbol=symbol, amount=total_amount).dict(exclude_none=True)
        payload = AddStakingRequest(symbol=symbol, amount=add_amount).json(exclude_none=True)
        response = AddStakingResponse.parse_raw(b=api.call(data=payload, params=path_params).content)
        return response

    def remove_staking(self, symbol: str, amount: int) -> RemoveStakingResponse:
        """
        Remove Staking finance/remove_staking
        :param symbol: e.g. "CRO"
        :param amount: e.g. 5000
        :return:
        """
        api = RemoveStakingApi(host=self.host, _session=self.session, exchange_token=self.exchange_token)
        payload = RemoveStakingRequest(symbol=symbol, amount=amount).json(exclude_none=True)
        response = RemoveStakingResponse.parse_raw(b=api.call(data=payload).content)
        return response

    def fee_rates(self) -> FeeRatesResponse:
        """
        Get fee rates, include tier, maker_rate, taker_rate, is_discount_fee and is_vip
        :return:
        """
        api = FeeRatesApi(host=self.host, _session=self.session, exchange_token=self.exchange_token)
        response = FeeRatesResponse.parse_raw(b=api.call().content)
        return response

    def get_charge_address(self, symbol: str, network: str) -> GetChargeAddressResponse:
        """get charge address

        Args:
            symbol (str): currency code e.g: CRO
            network (str): network name e.g: ERC20

        Returns:
            GetChargeAddressResponse: get charge address response
        """
        api = GetChargeAddressApi(host=self.host, _session=self.session, exchange_token=self.exchange_token)
        payload = GetChargeAddressRequest(symbol=symbol, network=network).json(exclude_none=True)
        response = GetChargeAddressResponse.parse_raw(b=api.call(data=payload).content)
        return response

    def v5_account_balance(self) -> AccountBalanceResponse:
        """get acount balance

        Returns:
            AccountBalanceResponse: account balance response
        """
        api = V5AccountBalanceApi(host=self.host, _session=self.session, exchange_token=self.exchange_token)
        response = AccountBalanceResponse.parse_raw(b=api.call().content)
        return response

    def do_withdraw(
        self,
        address_id: int,
        fee: float,
        amount: str,
        google_code: str,
        symbol: str,
        sms_otp: str,
        sms_auth_code: str = "",
        is_owner_of_address: bool = True,
        address_type_id: int = 3,
    ) -> DoWithdrawResponse:
        """do withdraw

        Args:
            address_id (int): address id
            fee (str): fee amount
            amount (str): withdraw amount
            google_code (str): google otp code
            sms_auth_code (str): null
            symbol (str): currency code
            sms_otp (str): sms opt code
            is_owner_of_address (bool): is owner of address
            address_type_id (int): address type 2 for other, 3 for crypto.com

        Returns:
            DoWithdrawResponse: DoWithdrawResponse
        """
        api = DoWithdrawApi(host=self.host, _session=self.session, exchange_token=self.exchange_token)
        payload = DoWithdrawRequest(
            addressId=address_id,
            fee=fee,
            amount=amount,
            googleCode=google_code,
            smsAuthCode=sms_auth_code,
            symbol=symbol,
            smsOtp=sms_otp,
            isOwnerOfAddress=is_owner_of_address,
            addressTypeId=address_type_id,
        ).json(exclude_none=True)
        response = DoWithdrawResponse.parse_raw(b=api.call(data=payload).content)
        return response

    def get_deposit_withdrawal_history(
        self,
        coin_symbol: str = None,
        start_ts: int = None,
        end_ts: int = None,
        page: int = None,
        page_size: int = 10,
        type: str = None,  # Withdrawal, Deposit
    ) -> GetDepositWithdrawalHistoryResponse:
        """get deposit withdrawal history

        Args:
            coin_symbol (str, optional): coin name. Defaults to None.
            start_ts (int, optional): start timestamp. Defaults to None.
            end_ts (int, optional): start timestamp. Defaults to None.
            page (int, optional): page number. Defaults to None.
            page_size (int, optional): page size. Defaults to 10.
            type (str, optional): history type, DEPOSIT/WITHDRAWAL. Defaults to None.

        Returns:
            GetDepositWithdrawalHistoryResponse: GetDepositWithdrawalHistoryResponse
        """
        api = GetDepositWithdrawalHistoryApi(host=self.host, _session=self.session, exchange_token=self.exchange_token)
        params = GetDepositWithdrawalHistoryRequest(
            coin_symbol=coin_symbol,
            start_ts=start_ts,
            end_ts=end_ts,
            page=page,
            page_size=page_size,
            type=type,
        )
        response = GetDepositWithdrawalHistoryResponse.parse_raw(b=api.call(params=params).content)
        return response
