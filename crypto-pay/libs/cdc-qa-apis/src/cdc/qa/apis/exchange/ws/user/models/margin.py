from typing import List, Optional
from pydantic import Field, validator
from decimal import Decimal
from ...models import SubscribeResponseResult, SubscribeResponse, SubscribeRequest
from ....models import FrozenBaseModel


# user.margin.balance
class MarginBalanceDetailData(FrozenBaseModel):
    currency: str = Field(description="e.g. CRO")
    balance: Decimal = Field(description="Total balance")
    available: Decimal = Field(description="Available balance (e.g. not in orders, or locked, etc.)")
    order: Decimal = Field(description="Balance locked in orders")
    stake: Decimal = Field(description="Balance locked for staking (typically only used for CRO)")


class SubscribeUserMarginBalanceRequestParams(FrozenBaseModel):
    channels: List[str] = ["user.margin.balance"]


class SubscribeUserMarginBalanceRequest(SubscribeRequest):
    params: SubscribeUserMarginBalanceRequestParams = SubscribeUserMarginBalanceRequestParams()


class SubscribeUserMarginBalanceResponseResult(SubscribeResponseResult):
    channel: str = "user.margin.balance"
    subscription: str = "user.margin.balance"
    data: List[MarginBalanceDetailData] = Field()

    @validator("channel")
    def channel_match(cls, v):
        assert v == "user.margin.balance", f"channel expect:[user.margin.balance] actual:[{v}]!"
        return v

    @validator("subscription")
    def subscription_match(cls, v):
        assert v == "user.margin.balance", f"subscription expect:[user.margin.balance] actual:[{v}]!"
        return v


class SubscribeUserMarignBalanceResponse(SubscribeResponse):
    result: SubscribeUserMarginBalanceResponseResult = Field(default=None)


# user.margin.order.{instrument_name}
class SubscribeUserMarginOrderInstrumentRequestParams(FrozenBaseModel):
    channels: List[str] = Field(...)


class SubscribeUserMarginOrderInstrumentRequest(SubscribeRequest):
    params: SubscribeUserMarginOrderInstrumentRequestParams = Field(...)


class SubscibeUserMarginOrderInstrumentData(FrozenBaseModel):
    order_id: str = Field(description="Order ID")
    client_oid: str = Field(description="(Optional) Client order ID if included in request")
    create_time: int = Field(description="Order creation time (Unix timestamp)")
    update_time: int = Field(description="Order update time (Unix timestamp)")
    status: str = Field(description="ACTIVE, CANCELED, FILLED, REJECTED or EXPIRED")
    reason: Optional[str] = Field(
        description="Reason code (see 'Response and Reason Codes') -- only for REJECTED orders"
    )
    type: str = Field(description="LIMIT, MARKET, STOP_LOSS, STOP_LIMIT, TAKE_PROFIT, TAKE_PROFIT_LIMIT")
    side: str = Field(description="BUY or SELL")
    instrument_name: str = Field(description="e.g. ETH_CRO, BTC_USDT")
    price: Decimal = Field(description="Price specified in the order")
    quantity: Decimal = Field(description="Quantity specified in the order")
    cumulative_quantity: Decimal = Field(description="Cumulative executed quantity (for partially filled orders)", ge=0)
    cumulative_value: Decimal = Field(description="Cumulative executed value (for partially filled orders)", ge=0)
    avg_price: Decimal = Field(description="Average filled price. If none is filled, returns 0", ge=0)
    fee_currency: str = Field(description="Currency used for the fees (e.g. CRO)")
    time_in_force: str = Field(description="GOOD_TILL_CANCEL, FILL_OR_KILL or IMMEDIATE_OR_CANCEL")
    exec_inst: str = Field(description="Empty or POST_ONLY (Limit Orders Only)")
    trigger_price: Optional[Decimal] = Field(description="Used for trigger-related orders")


class SubscribeUserMarginOrderInstrumentResponseResult(FrozenBaseModel):
    instrument_name: str = Field(description="e.g. ETH_CRO, BTC_USDT")
    subscription: str = Field(description="user.margin.order.{instrument_name} -- even in the all case")
    channel: str = Field(description="user.margin.order")
    data: List[SubscibeUserMarginOrderInstrumentData] = Field()

    @validator("subscription")
    def subscription_match(cls, v, values):
        expect = f"user.margin.order.{values['instrument_name']}"
        assert v == expect, f"subscription expect:[{expect}] actual:[{v}]!"
        return v

    @validator("channel")
    def channel_match(cls, v):
        assert v == "user.margin.order", f"channel expect:[user.margin.order] actual:[{v}]!"
        return v


class SubscribeUserMarginOrderInstrumentResponse(SubscribeResponse):
    result: SubscribeUserMarginOrderInstrumentResponseResult = Field()


# user.margin.trade.{instrument_name}
class SubscribeUserMarginTradeInstrumentRequestParams(FrozenBaseModel):
    channels: List[str] = Field(...)


class SubscribeUserMarginTradeInstrumentRequest(SubscribeRequest):
    params: SubscribeUserMarginTradeInstrumentRequestParams = Field(...)


class SubscribeUserMarginTradeInstrumentData(FrozenBaseModel):
    side: str = Field(description="BUY or SELL")
    fee: Decimal = Field(description="Trade fee")
    trade_id: str = Field(description="Trade id")
    create_time: int = Field(description="Trade creation time")
    traded_price: Decimal = Field(description="Executed trade price")
    traded_quantity: Decimal = Field(description="Executed trade quantity")
    fee_currency: str = Field(description="Currency used for the fees (e.g. CRO)")
    order_id: str = Field(description="Order ID")


class SubscribeUserMarginTradeInstrumentResponseResult(FrozenBaseModel):
    instrument_name: str = Field(description="e.g. ETH_CRO, BTC_USDT")
    subscription: str = Field(description="user.margin.trade.{instrument_name} -- even in the all case")
    channel: str = Field(description="user.margin.trade")
    data: List[SubscribeUserMarginTradeInstrumentData] = Field()

    @validator("subscription")
    def subscription_match(cls, v, values):
        expect = f"user.margin.trade.{values['instrument_name']}"
        assert v == expect, f"subscription expect:[{expect}] actual:[{v}]!"
        return v

    @validator("channel")
    def channel_match(cls, v):
        assert v == "user.margin.trade", f"channel expect:[user.margin.trade] actual:[{v}]!"
        return v


class SubscribeUserMarginTradeInstrumentResponse(SubscribeResponse):
    result: SubscribeUserMarginTradeInstrumentResponseResult = Field()
