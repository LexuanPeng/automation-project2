from typing import List, Optional
from pydantic import Field, validator

from ...models import SubscribeResponseResult, SubscribeResponse, SubscribeRequest
from ....models import FrozenBaseModel, ExchangeRequest, ExchangeResponse


class PositionBalanceDetail(FrozenBaseModel):
    quantity: str = Field(description="quantity")
    collateral_weight: str = Field(description="collateralWeight")
    collateral_amount: str = Field(description="collateralAmount")
    market_value: str = Field(description="marketValue")
    max_withdrawal_balance: str = Field(description="maxWithdrawalBalance")
    instrument_name: str = Field(description="maxWithdrawalBalance")
    reserved_qty: Optional[str] = Field(description="reserved_qty")
    hourly_interest_rate: Optional[str] = Field(description="hourly_interest_rate")


class UserPositionBalanceDetailAboutPositionsInfo(FrozenBaseModel):
    account_id: str = Field(description="Account ID")
    quantity: str = Field(description="Position quantity")
    cost: str = Field(description="Position cost or value in USD")
    open_position_pnl: str = Field(description="Profit and loss for the open position")
    open_pos_cost: str = Field(description="Open pos cost")
    session_pnl: str = Field(description="Profit and loss in the current trading session")
    update_timestamp_ms: int = Field(description="Update time (Unix timestamp)")
    instrument_name: str = Field(description="e.g. BTCUSD-PERP")
    type: str = Field(description="e.g. PERPETUAL_SWAP")


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
    total_collateral_value: str = Field(description="Collateral Value")
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
    position_balances: Optional[List[PositionBalanceDetail]] = Field()
    balances: Optional[List[PositionBalanceDetail]] = Field()
    positions: Optional[List[UserPositionBalanceDetailAboutPositionsInfo]] = Field()


class UserPositionBalanceDetailAboutBalancesInfo(FrozenBaseModel):
    instrument_name: str = Field(description="instrument name of the balance e.g. BTC")
    quantity: str = Field(description="Quantity of the collateral")
    update_timestamp_ms: int = Field(description="Update time (Unix timestamp)")


class UserPositionBalanceDetail(FrozenBaseModel):
    balances: List[UserPositionBalanceDetailAboutBalancesInfo] = Field()
    positions: Optional[List[UserPositionBalanceDetailAboutPositionsInfo]] = Field()


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
class PrivateUserBalanceRequest(ExchangeRequest):
    method: str = "private/user-balance"
    params: dict = {}


class PrivateUserBalanceResponseResult(FrozenBaseModel):
    data: List[TotalBalanceDetail] = Field()


class PrivateUserBalanceResponse(ExchangeResponse):
    result: PrivateUserBalanceResponseResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/user-balance"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# user.account_risk
class SubscribeUserAccountRiskRequestParams(FrozenBaseModel):
    channels: List[str] = ["user.account_risk"]


class SubscribeUserAccountRiskRequest(SubscribeRequest):
    params: SubscribeUserAccountRiskRequestParams = SubscribeUserAccountRiskRequestParams()


class SubscribeUserAccountRiskResponseResult(SubscribeResponseResult):
    channel: str = "user.account_risk"
    subscription: str = "user.account_risk"
    data: List[TotalBalanceDetail] = Field()

    @validator("channel")
    def channel_match(cls, v):
        assert v == "user.account_risk", f"channel expect:[user.account_risk] actual:[{v}]!"
        return v

    @validator("subscription")
    def subscription_match(cls, v):
        assert v == "user.account_risk", f"subscription expect:[user.account_risk] actual:[{v}]!"
        return v


class SubscribeUserAccountRiskResponse(SubscribeResponse):
    result: SubscribeUserAccountRiskResponseResult = Field(default=None)


# user.position_balance
class SubscribeUserPositionBalanceRequestParams(FrozenBaseModel):
    channels: List[str] = ["user.position_balance"]


class SubscribeUserPositionBalanceRequest(SubscribeRequest):
    params: SubscribeUserPositionBalanceRequestParams = SubscribeUserPositionBalanceRequestParams()


class SubscribeUserPositionBalanceResponseResult(SubscribeResponseResult):
    channel: str = "user.position_balance"
    subscription: str = "user.position_balance"
    data: List[UserPositionBalanceDetail] = Field()

    @validator("channel")
    def channel_match(cls, v):
        assert v == "user.position_balance", f"channel expect:[user.position_balance] actual:[{v}]!"
        return v

    @validator("subscription")
    def subscription_match(cls, v):
        assert v == "user.position_balance", f"subscription expect:[user.position_balance] actual:[{v}]!"
        return v


class SubscribeUserPositionBalanceResponse(SubscribeResponse):
    result: SubscribeUserPositionBalanceResponseResult = Field(default=None)
