from typing import List, Optional
from pydantic import Field, validator

from ...models import SubscribeResponseResult, SubscribeResponse, SubscribeRequest
from ....models import FrozenBaseModel, DerivativesRequest, DerivativesResponse


class PositionBalanceDetail(FrozenBaseModel):
    quantity: str = Field(description="quantity")
    collateral_weight: str = Field(description="collateralWeight")
    collateral_amount: str = Field(description="collateralAmount")
    market_value: str = Field(description="marketValue")
    max_withdrawal_balance: str = Field(description="maxWithdrawalBalance")
    instrument_name: str = Field(description="maxWithdrawalBalance")
    reserved_qty: Optional[str] = Field(description="reserved_qty")


class TotalBalanceDetail(FrozenBaseModel):
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
    position_balances: List[PositionBalanceDetail] = Field()
    total_collateral_value: str = Field(description="Collateral Value")


class SubscribeUserBalanceRequestParams(FrozenBaseModel):
    channels: List[str] = ["user.balance"]


class SubscribeUserBalanceRequest(SubscribeRequest):
    params: SubscribeUserBalanceRequestParams = SubscribeUserBalanceRequestParams()


class SubscribeUserBalanceResponseResult(SubscribeResponseResult):
    channel: str = "user.balance"
    subscription: str = "user.balance"
    data: List[TotalBalanceDetail] = Field()

    @validator("channel")
    def channel_match(cls, v):
        assert v == "user.balance", f"channel expect:[user.balance] actual:[{v}]!"
        return v

    @validator("subscription")
    def subscription_match(cls, v):
        assert v == "user.balance", f"subscription expect:[user.balance] actual:[{v}]!"
        return v


class SubscribeUserBalanceResponse(SubscribeResponse):
    result: SubscribeUserBalanceResponseResult = Field(default=None)


# private/user-balance
class PrivateUserBalanceRequest(DerivativesRequest):
    method: str = "private/user-balance"
    params: dict = {}


class PrivateUserBalanceResponseResult(FrozenBaseModel):
    data: List[TotalBalanceDetail] = Field()


class PrivateUserBalanceResponse(DerivativesResponse):
    result: PrivateUserBalanceResponseResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/user-balance"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v
