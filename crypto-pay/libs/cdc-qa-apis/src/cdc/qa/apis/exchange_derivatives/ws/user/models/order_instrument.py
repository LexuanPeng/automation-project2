from typing import List, Optional
from pydantic import Field
from ....models import FrozenBaseModel
from ...models import SubscribeResponse, SubscribeRequest


class SubscribeUserOrderInstrumentRequestParams(FrozenBaseModel):
    channels: List[str] = Field(...)


class SubscribeUserOrderInstrumentRequest(SubscribeRequest):
    params: SubscribeUserOrderInstrumentRequestParams = Field(...)


class OrderInstrumentDetail(FrozenBaseModel):
    account_id: str
    order_id: str
    client_oid: str
    order_type: str = Field(description="order type, such as LIMIT")
    time_in_force: str = Field(description="time in force, such as GOOD_TILL_CANCEL")
    side: str = Field(description="side, such as BUY, SELL")
    exec_inst: List[str]
    quantity: str = Field(description="order quantity")
    limit_price: str = Field(description="order limit price")
    order_value: str
    maker_fee_rate: str
    taker_fee_rate: str
    avg_price: str
    cumulative_quantity: str
    cumulative_value: str
    cumulative_fee: str
    status: str = Field(description="order status ACTIVE")
    update_user_id: str
    order_date: str
    instrument_name: str
    fee_instrument_name: str
    create_time: int
    create_time_ns: int
    update_time: int


class SubscribeUserOrderInstrumentResponseResult(FrozenBaseModel):
    instrument_name: Optional[str] = Field(description="BTCUSD-PERP")
    channel: str = Field()
    subscription: str = Field()
    data: List[OrderInstrumentDetail] = Field()

    # @validator("subscription")
    # def subscription_match(cls, v, values):
    #     expect = f"user.order.{values['instrument_name']}"
    #     assert v == expect, f"subscription expect:[{expect}] actual:[{v}]!"
    #     return v
    #
    # @validator("channel")
    # def channel_match(cls, v, values):
    #     expect = f"user.order.{values['instrument_name']}"
    #     assert v == expect, f"channel expect:[{expect}] actual:[{v}]!"
    #     return v


class SubscribeUserOrderInstrumentResponse(SubscribeResponse):
    result: SubscribeUserOrderInstrumentResponseResult = Field(default=None)
