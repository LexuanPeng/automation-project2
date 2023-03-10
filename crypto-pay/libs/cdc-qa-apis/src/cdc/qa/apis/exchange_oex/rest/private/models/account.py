from decimal import Decimal
from enum import Enum
from typing import List, Optional, Dict

from cdc.qa.apis.exchange_oex.models import (
    ExchangeRequestParams,
    ExchangeResponse,
    ExchangeSignedRequest,
    FrozenBaseModel,
)
from pydantic import Field, validator


# private/user-balance
class PositionBalance(FrozenBaseModel):
    quantity: str = Field(description="quantity")
    collateral_weight: str = Field(description="collateralWeight")
    collateral_amount: str = Field(description="collateralAmount")
    market_value: str = Field(description="marketValue")
    max_withdrawal_balance: str = Field(description="maxWithdrawalBalance")
    instrument_name: str = Field(description="instrument Name")
    reserved_qty: Optional[str] = Field(description="reserved_qty")
    hourly_interest_rate: Optional[str] = Field(description="hourly_interest_rate")


class TotalBalance(FrozenBaseModel):
    account: Optional[str] = Field(description="Sub account ID")
    instrument_name: str = Field(description="instrument name of the balance e.g. USD_Stable_Coin")
    total_available_balance: str = Field(
        description="Balance that user can open new order (Margin Balance - Initial Margin)"
    )
    total_margin_balance: str = Field(
        description="Balance for the margin calculation (Wallet Balance + Unrealized PnL)"
    )
    total_initial_margin: str = Field(
        description="Total initial margin requirement for all positions and all open orders"
    )
    total_maintenance_margin: str = Field(description="Total maintenance margin requirement for all positions")
    total_position_cost: str = Field(description="Position value in USD")
    total_cash_balance: str = Field(description="Wallet Balance (Deposits - Withdrawals + Realized PnL - Fees)")
    total_collateral_value: Optional[str] = Field(description="Collateral Balance")
    total_session_unrealized_pnl: str = Field(
        description="""Current unrealized profit and loss from all open positions
        (calculated with Mark Price and Avg Price)"""
    )
    total_session_realized_pnl: str = Field(
        description="""Current realized profit and loss from all open positions
        (calculated with Mark Price and Avg Price)"""
    )
    is_liquidating: bool = Field(description="Describes whether the account is under liquidation")
    total_effective_leverage: str = Field(
        description="The actual leverage used (all open positions combined), i.e. position size / margin balance"
    )
    position_limit: str = Field(description="Maximum position size allowed (for all open positions combined)")
    used_position_limit: str = Field(
        description="Combined position size of all open positions + order exposure on all instruments"
    )
    position_balances: List[PositionBalance] = Field()


class UserBalanceRequestBody(ExchangeSignedRequest):
    method: str = "private/user-balance"
    params: ExchangeRequestParams = Field()


class UserBalanceResult(FrozenBaseModel):
    data: List[TotalBalance] = Field()


class UserBalanceResponse(ExchangeResponse):
    result: UserBalanceResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/user-balance"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/get-subaccount-balances
class GetSubAccountBalancesRequestBody(ExchangeSignedRequest):
    method: str = "private/get-subaccount-balances"
    params: ExchangeRequestParams = Field()


class GetSubAccountBalancesResult(FrozenBaseModel):
    data: List[TotalBalance] = Field()


class GetSubAccountBalancesResponse(ExchangeResponse):
    result: GetSubAccountBalancesResult = Field()


# private/user-balance-history
class BalanceHistory(FrozenBaseModel):
    t: str = Field(description="timestamp")
    c: str = Field(description="total cash balance")


class UserBalanceHistoryRequestParams(ExchangeRequestParams):
    timeframe: Optional[str] = Field(description="H1 means every hour, D1 means every day. Omit for 'D1'")
    end_time: Optional[int] = Field(
        description="Can be millisecond or nanosecond. Exclusive. If not provided, will be current time."
    )
    limit: Optional[int] = Field(
        description="If timeframe is D1, max limit will be 30 (days)."
        " If timeframe is H1, max limit will be 120 (hours)."
    )


class UserBalanceHistoryRequestBody(ExchangeSignedRequest):
    method: str = "private/user-balance-history"
    params: UserBalanceHistoryRequestParams = {}


class UserBalanceHistoryResult(FrozenBaseModel):
    instrument_name: str = Field(description="instrument name")
    data: List[BalanceHistory] = Field()


class UserBalanceHistoryResponse(ExchangeResponse):
    result: UserBalanceHistoryResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/user-balance-history"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/change-account-leverage
class ChangeAccountLeverageRequestParams(ExchangeRequestParams):
    account_id: str = Field(description="Account ID")
    leverage: int = Field(description="maximum leverage to be used for the account e.g. 100, etc.")


class ChangeAccountLeverageRequestBody(ExchangeSignedRequest):
    method: str = "private/change-account-leverage"
    params: ChangeAccountLeverageRequestParams = Field()


class ChangeAccountLeverageResponse(ExchangeResponse):
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/change-account-leverage"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/create-withdrawal
class CreateWithdrawalRequestParams(FrozenBaseModel):
    client_wid: Optional[str] = Field(description="Optional Client withdrawal ID")
    currency: str = Field(description="E.g. BTC, CRO")
    amount: Decimal
    address: str = Field(description="Address with Address Tag (if any)")
    address_tag: Optional[str] = Field(
        description="Secondary address identifier for coins like XRP, XLM etc. Also known as memo or tags."
    )
    network_id: Optional[str] = Field(
        description="Select the desired network, require the address to be whitelisted first."
        " See default_network and network in get-currency-networks for the value."
    )


class CreateWithdrawalRequest(ExchangeSignedRequest):
    method: str = "private/create-withdrawal"
    params: CreateWithdrawalRequestParams = Field()


class CreateWithdrawalResult(FrozenBaseModel):
    id: int = Field(description="Newly created withdrawal ID")
    client_wid: Optional[str] = Field(description="(Optional) if a Client withdrawal ID was provided in the request")
    currency: str = Field(description="E.g. BTC, CRO, ETH")
    amount: Decimal
    fee: Decimal
    address: str = Field(description="Address with Address Tag (if any)")
    create_time: int
    network_id: Optional[str]


class CreateWithdrawalResponse(ExchangeResponse):
    result: CreateWithdrawalResult = Field()


# private/get-currency-networks
class NetworkList(FrozenBaseModel):
    network_id: str = Field(description="the network id, can be used in create-withdrawal")
    withdraw_enabled: bool = Field()
    deposit_enabled: bool = Field()
    withdrawal_fee: Decimal = Field(default=None)
    min_withdrawal_amount: Decimal
    confirmation_required: int = Field(description="confirmation blocks count")


class CurrencyMapDetail(FrozenBaseModel):
    full_name: str = Field(description="e.g. SHIBA INU")
    default_network: str = Field(
        default=None,
        description="If network is not provided in create-withdrawal, it will search for default_network, "
        "if there is more than 1 network available.",
    )
    network_list: List[NetworkList] = Field(description="A list of networks")


class CurrencyMap(FrozenBaseModel):
    __root__: Dict[str, CurrencyMapDetail]

    def __iter__(self):
        return iter(self.__root__)

    def __getattr__(self, item):
        return self.__root__.get(item, None)


class GetCurrencyNetworksRequest(ExchangeSignedRequest):
    method: str = "private/get-currency-networks"
    params: dict = {}


class GetCurrencyNetworksResult(FrozenBaseModel):
    update_time: str
    currency_map: CurrencyMap


class GetCurrencyNetworksResponse(ExchangeResponse):
    result: GetCurrencyNetworksResult = Field()


# private/get-deposit-address
class DepositAddressStatus(Enum):
    """0 - Inactive   1 - Active"""

    INACTIVE = "0"
    ACTIVE = "1"


class GetDepositAddressRequestParams(FrozenBaseModel):
    currency: Optional[str] = Field(description="E.g. BTC, CRO")


class GetDepositAddressRequest(ExchangeSignedRequest):
    method: str = "private/get-deposit-address"
    params: GetDepositAddressRequestParams = Field()


class DepositAddressDetail(FrozenBaseModel):
    id: int = Field(description="Newly created address ID")
    currency: str = Field(description="E.g. BTC, CRO")
    network: str = Field(description="E.g. ETH, CRO")
    address: str = Field(description="Address with Address Tag (if any)")
    create_time: int
    status: DepositAddressStatus = Field(description="""0 - Inactive   1 - Active""")


class GetDepositAddressResult(FrozenBaseModel):
    deposit_address_list: List[DepositAddressDetail] = Field()


class GetDepositAddressResponse(ExchangeResponse):
    result: GetDepositAddressResult = Field()


# private/create-subaccount-transfer
class CreateSubaccountTransferRequestParams(ExchangeRequestParams):
    from_side: str = Field(description="Account ID", alias="from")
    to: str = Field(description="Account ID")
    currency: str = Field(description="E.g. BTC, CRO")
    amount: str = Field(description="Amount")


class CreateSubaccountTransferRequest(ExchangeSignedRequest):
    method: str = "private/create-subaccount-transfer"
    params: CreateSubaccountTransferRequestParams = Field()


class CreateSubaccountTransferResponse(ExchangeResponse):
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/create-subaccount-transfer"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/create-subaccount-multi-transfer
class CreateSubaccountMultiTransferRequestParams(ExchangeRequestParams):
    currencies: List[str] = Field(description="E.g. ['BTC','ETH']")
    from_side: List[str] = Field(description="Account ID, e.g ['id_01', id_02']", alias="from")
    to: str = Field(description="Account ID")


class CreateSubaccountMultiTransferRequest(ExchangeSignedRequest):
    method: str = "private/create-subaccount-multi-transfer"
    params: CreateSubaccountMultiTransferRequestParams = Field()


class CreateSubaccountMultiTransferResponse(ExchangeResponse):
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/create-subaccount-multi-transfer"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/get-accounts
class AccountInfo(FrozenBaseModel):
    uuid: str = Field(description="Sub account uuid")
    master_account_uuid: Optional[str] = Field(description="Master account uuid")
    margin_account_uuid: Optional[str] = Field(description="(optional) Margin account uuid")
    label: Optional[str] = Field(description="Sub account label")
    enabled: bool = Field(description="true or false")
    tradable: bool = Field(description="true or false")
    name: str = Field(description="Name of sub account")
    email: Optional[str] = Field(description="Email of sub account")
    mobile_number: Optional[str] = Field(description="Mobile number of sub account")
    country_code: str = Field(description="Country Code of sub account")
    address: Optional[str] = Field(description="DEFAULT or DISABLED")
    margin_access: str = Field(description="DEFAULT or DISABLED")
    derivatives_access: str = Field(description="DEFAULT or DISABLED")
    create_time: str = Field(description="Creation timestamp (milliseconds since the Unix epoch)")
    update_time: str = Field(description="Last update timestamp (milliseconds since the Unix epoch)")
    two_fa_enabled: bool = Field(description="true or false")
    kyc_level: str = Field(description="Kyc Level")
    suspended: bool = Field(description="true or false")
    terminated: bool = Field(description="true or false")
    system_label: Optional[str] = Field(
        description="""Possible values if specified:
                        FORMER_MASTER_MARGIN
                        FORMER_MASTER_DERIVATIVES
                        FORMER_SUBACCOUNT_SPOT
                        FORMER_SUBACCOUNT_MARGIN
                        FORMER_SUBACCOUNT_DERIVATIVES
                        ONEEX_SUBACCOUNT
                        See Unified Wallet and System Label section for details
                        """
    )


class GetAccountRequestBody(ExchangeSignedRequest):
    method: str = "private/get-accounts"
    params: dict = {}


class GetAccountResult(FrozenBaseModel):
    master_account: AccountInfo = Field()
    sub_account_list: List[AccountInfo] = Field()


class GetAccountResponse(ExchangeResponse):
    result: GetAccountResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/get-accounts"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/get-account-info
class GetAccountInfoRequestBody(ExchangeSignedRequest):
    method: str = "private/get-account-info"
    params: ExchangeRequestParams = Field()


class GetAccountInfoDetail(FrozenBaseModel):
    id: str = Field("7f1a1bdd-e454-4c3c-86cc-c44061d75fcc")
    parent_deriv_account_id: str = Field("00000000-0000-0000-0000-000000000000")
    max_leverage: int = Field()
    enabled_spot_margin: bool = Field()
    enabled_deriv_trading: bool = Field()


class GetAccountInfoResponse(ExchangeResponse):
    method: str
    result: List[GetAccountInfoDetail] = Field()

    @validator("method")
    def check_method(cls, v):
        method = "private/get-account-info"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


class GetRiskInfoRequestParams(ExchangeRequestParams):
    instrument_name: str = Field(description="margin instrument name")


class GetRiskInfoRequestBody(ExchangeSignedRequest):
    method: str = "private/get-risk-info"
    params: GetRiskInfoRequestParams = Field()


class RiskInfoResult(FrozenBaseModel):
    base_ccy: str
    quote_ccy: str
    order_max_margin_base_ccy_buy_qty: str
    order_max_margin_quote_ccy_buy_qty: str
    order_max_margin_base_ccy_sell_qty: str
    order_max_margin_quote_ccy_sell_qty: str


class GetRiskInfoResponse(ExchangeResponse):
    method: str
    result: RiskInfoResult

    @validator("method")
    def check_method(cls, v):
        method = "private/get-risk-info"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/create-intra-transfer
class CreateIntraTransferRequestParams(ExchangeRequestParams):
    to: str = Field(description="transfer to")
    currency: str = Field(description="transfer currency")
    amount: str = Field(description="transfer amount")


class CreateIntraTransferRequestBody(ExchangeSignedRequest):
    method: str = "private/create-intra-transfer"
    params: CreateIntraTransferRequestParams = Field()


class CreateIntraTransferResponseResult(FrozenBaseModel):
    to: str = Field(description="transfer to")
    currency: str = Field(description="transfer currency")
    amount: str = Field(description="transfer amount")


class CreateIntraTransferResponse(ExchangeResponse):
    method: str
    result: CreateIntraTransferResponseResult

    @validator("method")
    def check_method(cls, v):
        method = "private/create-intra-transfer"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v
