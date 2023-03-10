from typing import List, Optional

from cdc.qa.apis.exchange_derivatives.models import DerivativesResponse, DerivativesSignedRequest, FrozenBaseModel
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


class TotalBalance(FrozenBaseModel):
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
    total_session_unrealized_pnl: str = Field(
        description="""Current unrealized profit and loss from all open positions
        (calculated with Mark Price and Avg Price)"""
    )
    total_session_realized_pnl: str = Field(
        description="""Current realized profit and loss from all open positions
        (calculated with Mark Price and Avg Price)"""
    )
    is_liquidating: bool = Field(description="Describes whether the account is under liquidation")
    position_balances: List[PositionBalance] = Field()


class UserBalanceRequestBody(DerivativesSignedRequest):
    method: str = "private/user-balance"
    params: dict = {}


class UserBalanceResult(FrozenBaseModel):
    data: List[TotalBalance] = Field()


class UserBalanceResponse(DerivativesResponse):
    result: UserBalanceResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/user-balance"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


class GetSubAccountBalancesRequestBody(DerivativesSignedRequest):
    method: str = "private/get-subaccount-balances"
    params: dict = {}


class GetSubAccountBalancesResult(FrozenBaseModel):
    data: List[TotalBalance] = Field()


class GetSubAccountBalancesResponse(DerivativesResponse):
    result: GetSubAccountBalancesResult = Field()


# private/change-account-leverage
class ChangeAccountLeverageRequestParams(FrozenBaseModel):
    account_id: str = Field(description="Account ID")
    leverage: int = Field(description="maximum leverage to be used for the account e.g. 100, etc.")


class ChangeAccountLeverageRequestBody(DerivativesSignedRequest):
    method: str = "private/change-account-leverage"
    params: ChangeAccountLeverageRequestParams = Field()


class ChangeAccountLeverageResponse(DerivativesResponse):
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/change-account-leverage"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/get-account-info
class GetAccountInfoRequestBody(DerivativesSignedRequest):
    method: str = "private/get-account-info"
    params: dict = {}


class GetAccountInfoDetail(FrozenBaseModel):
    id: str = Field("7f1a1bdd-e454-4c3c-86cc-c44061d75fcc")
    parent_deriv_account_id: str = Field("00000000-0000-0000-0000-000000000000")
    max_leverage: int = Field()
    enabled_spot_margin: bool = Field()
    enabled_deriv_trading: bool = Field()


class GetAccountInfoResponse(DerivativesResponse):
    method: str
    result: List[GetAccountInfoDetail] = Field()

    @validator("method")
    def check_method(cls, v):
        method = "private/get-account-info"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v
