from typing import List, Optional
from pydantic import Field, validator
from ....models import FrozenBaseModel
from ...models import SubscribeRequest, SubscribeResponse


# user.order.{instrument_name}
class SubscribeUserOrderInstrumentRequestParams(FrozenBaseModel):
    channels: List[str] = Field(...)


class SubscribeUserOrderInstrumentRequest(SubscribeRequest):
    params: SubscribeUserOrderInstrumentRequestParams = Field(...)


class OrderInstrumentDetail(FrozenBaseModel):
    account_id: str = Field(description="Account ID")
    order_id: str = Field(description="Order ID")
    client_oid: str = Field(description="Client Order ID")
    order_type: str = Field(description="MARKET, LIMIT, STOP_LOSS, STOP_LIMIT, TAKE_PROFIT, TAKE_PROFIT_LIMIT")
    time_in_force: str = Field(description="time in force, such as GOOD_TILL_CANCEL")
    side: str = Field(description="side, such as BUY, SELL")
    exec_inst: List[str] = Field(description="POST_ONLY, REDUCE_ONLY, LIQUIDATION")
    quantity: str = Field(description="Quantity specified in the order")
    limit_price: Optional[str] = Field(description="Limit price specified in the order")
    order_value: str = Field(description="Order value")
    maker_fee_rate: str = Field(description="User's maker fee rate")
    taker_fee_rate: str = Field(description="User's taker fee rate")
    avg_price: str = Field(description="Average price")
    cumulative_quantity: str = Field(description="Cumulative executed quantity")
    cumulative_value: str = Field(description="Cumulative executed value")
    cumulative_fee: str = Field(description="Cumulative executed fee")
    status: str = Field(description="Order status:NEW, PENDING, REJECTED,ACTIVE,CANCELED,FILLED,EXPIRED")
    update_user_id: str = Field(description="Updated user")
    order_date: str = Field(description="Order creation date")
    instrument_name: str = Field(description="e.g. BTCUSD-PERP")
    fee_instrument_name: str = Field(description="Currency used for the fees")
    create_time: int = Field(description="Order creation timestamp")
    create_time_ns: int = Field(description="Order creation timestamp (nanosecond)")
    update_time: int = Field(description="Order update timestamp")


class SubscribeUserOrderInstrumentResponseResult(FrozenBaseModel):
    instrument_name: Optional[str] = Field(description="BTCUSD-PERP")
    channel: str = Field()
    subscription: str = Field()
    data: List[OrderInstrumentDetail] = Field()

    @validator("subscription")
    def subscription_match(cls, v: str, values):
        # instrument_name = values.get("instrument_name")
        # expect = ["user.order"]
        # expect = expect if instrument_name is None else expect.append(f"user.order.{instrument_name}")
        # assert v in expect, f"subscription expect in:[{expect}] actual:[{v}]!"
        assert v.startswith("user.order"), f"subscription expect start with [user.order] actual:[{v}]!"
        return v

    @validator("channel")
    def channel_match(cls, v: str, values):
        # instrument_name = values.get("instrument_name")
        # expect = ["user.order"]
        # expect = expect if instrument_name is None else expect.append(f"user.order.{instrument_name}")
        # assert v in expect, f"channel expect:[{expect}] actual:[{v}]!"
        assert v.startswith("user.order"), f"channel expect start with [user.order] actual:[{v}]!"
        return v


class SubscribeUserOrderInstrumentResponse(SubscribeResponse):
    result: SubscribeUserOrderInstrumentResponseResult = Field(default=None)
