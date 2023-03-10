from typing import List
from pydantic import Field, validator
from ....models import FrozenBaseModel
from ...models import SubscribeResponse, SubscribeRequest


class SubscribeTradeInstrumentRequestParams(FrozenBaseModel):
    channels: List[str] = Field(...)


class SubscribeTradeInstrumentRequest(SubscribeRequest):
    params: SubscribeTradeInstrumentRequestParams = Field(...)


class TradeInstrumentDetail(FrozenBaseModel):
    s: str = Field(description="Side (buy or sell)")
    p: str = Field(description="Trade price")
    q: str = Field(description="Trade quantity")
    t: int = Field(description="Trade timestamp")
    d: str = Field(description="of number	Trade ID")
    i: str = Field(description="Instrument name")


class SubscribeTradeInstrumentResponseResult(FrozenBaseModel):
    instrument_name: str = Field(description="e.g BTCUSD-PERP")
    channel: str = "trade"
    subscription: str = Field()
    data: List[TradeInstrumentDetail] = Field()

    @validator("subscription")
    def subscription_match(cls, v, values):
        expect = f"trade.{values['instrument_name']}"
        assert v == expect, f"subscription expect:[{expect}] actual:[{v}]!"
        return v

    @validator("channel")
    def channel_match(cls, v):
        assert v == "trade", f"channel expect:[trade] actual:[{v}]!"
        return v


class SubscribeTradeInstrumentResponse(SubscribeResponse):
    result: SubscribeTradeInstrumentResponseResult = Field(default=None)
