from decimal import Decimal
from typing import Dict, Optional, Union, List

from pydantic import Field

from ..fe_models import FeExchangeRequest, FeExchangeResponse, FrozenBaseModel


class AddStakingRequest(FeExchangeRequest):
    symbol: str = Field(description="CRO")
    amount: int = Field(description="CRO Staking amount")


class AddStakingRequestPath(FrozenBaseModel):
    symbol: str = Field(description="CRO")
    amount: int = Field(description="CRO Staking total amount")


class AddStakingResponse(FeExchangeResponse):
    pass


class RemoveStakingRequest(FeExchangeRequest):
    symbol: str = Field(description="CRO")
    amount: int = Field(description="CRO Staking remove amount")


class RemoveStakingResponse(FeExchangeResponse):
    pass


class FeeRatesDataDetail(FrozenBaseModel):
    is_discounted_fee: bool
    is_vip: bool = Field(description="is vip user")
    maker_rate: Decimal = Field(description="Maker rate")
    taker_rate: Decimal = Field(description="Taker rate")
    tier: int = Field(description="user tier: 0 - 8")


class FeeRatesResponse(FeExchangeResponse):
    data: FeeRatesDataDetail = Field("fee rates detail")


# /finance/get_charge_address
class GetChargeAddressRequest(FeExchangeRequest):
    symbol: str = Field(description="CRO")
    network: str = Field(description="wallet address network")


class GetChargeAddressDataDetail(FrozenBaseModel):
    addressQRCode: str = Field(description="address QR Code")
    addressStr: str = Field(description="address str")
    addressSub: Optional[str]
    addressTag: Optional[str]
    addressTagQRCode: Optional[str]


class GetChargeAddressResponse(FeExchangeResponse):
    data: GetChargeAddressDataDetail = Field("fee rates detail")


# finance/v5/account_balance
class SymbolsDetail(FrozenBaseModel):
    available_balance: Decimal
    btc_equivalent: Decimal
    deposit_open: bool
    in_order_balance: Decimal
    is_fiat: bool
    open_order_balance: Decimal
    sort: int
    stake_balance: Decimal
    supercharger_balance: Decimal
    syndicate_balance: Decimal
    total_balance: Decimal
    usd_equivalent: Decimal
    withdraw_open: bool


class SymbolInfo(FrozenBaseModel):
    __root__: Dict[str, SymbolsDetail]

    def __iter__(self):
        return iter(self.__root__)

    def __getattr__(self, item):
        return self.__root__.get(item, None)


class AccountBalanceDataDetail(FrozenBaseModel):
    total_balance_in_btc: Decimal
    total_balance_in_usd: Decimal
    symbols: SymbolInfo


class AccountBalanceResponse(FeExchangeResponse):
    data: AccountBalanceDataDetail = Field("account balance detail")


# https://xdev-www.3ona.co/fe-ex-api/finance/do_withdraw
class DoWithdrawRequest(FeExchangeRequest):
    addressId: int = Field(description="addressId")
    fee: float = Field(description="fee")
    amount: str = Field(description="amount")
    googleCode: str = Field(description="googleCode")
    smsAuthCode: str = Field(description="smsAuthCode")
    symbol: str = Field(description="symbol")
    smsOtp: str = Field(description="smsOtp")
    isOwnerOfAddress: bool = Field(description="isOwnerOfAddress")
    addressTypeId: int = Field(description="addressTypeId")


class DoWithdrawResult(FrozenBaseModel):
    amount: str = Field(description="0.0001")
    coinSymbol: str = Field(description="BTC")
    address: str = Field(description="2N6JEjKsXT4hnK6nSYUKvQg96eVMKmxasBa")
    label: str = Field(description="addr_02")
    applyTime: str = Field(description="2022-11-30 07:43:54")


class DoWithdrawResponse(FeExchangeResponse):
    data: DoWithdrawResult = Field()


# https://xdev-www.3ona.co/fe-ex-api/get-deposit-withdrawal-history
class GetDepositWithdrawalHistoryRequest(FrozenBaseModel):
    coin_symbol: Optional[str] = Field(description="coin_symbol", default=None)
    start_ts: Optional[int] = Field(description="start_ts", default=None)
    end_ts: Optional[int] = Field(description="end_ts", default=None)
    page: Optional[int] = Field(description="page", default=None)
    page_size: Optional[int] = Field(description="page_size", default=None)
    type: Optional[str] = Field(description="type", default=None)


class DepositWithdrawalHistoryDetail(FrozenBaseModel):
    type: str = Field(description="WITHDRAWAL, DEPOSIT")
    coin_symbol: str = Field(description="BTC")
    amount: str = Field(description="0.0001")
    fee: str = Field(description="0.0004")
    to_address: str = Field(description="2N6JEjKsXT4hnK6nSYUKvQg96eVMKmxasBa")
    withdrawal_address_label: Union[str, None] = Field(description="addr_02")
    withdrawal_reject_reason: Union[str, None] = Field(description="")
    network: str = Field(description="BTC")
    txid: str = Field(description="4a3085fa432d9e4066e7487a4131f977a10d97a6c7d3fe5349f7f96ed2147eb7")
    explorer_url: str = Field(description="/transaction/4a3085fa432d9e4066e7487a4131f977a10d97a6c7d3fe5349f7f96ed214")
    status: int = Field(description="")
    created_at: int = Field(description="")
    updated_at: int = Field(description="")


class GetDepositWithdrawalHistoryData(FrozenBaseModel):
    count: int
    history_list: List[DepositWithdrawalHistoryDetail]
    page: int
    page_size: int


class GetDepositWithdrawalHistoryResult(FrozenBaseModel):
    data: GetDepositWithdrawalHistoryData = Field()


class GetDepositWithdrawalHistoryResponse(FeExchangeResponse):
    result: GetDepositWithdrawalHistoryResult = Field()
