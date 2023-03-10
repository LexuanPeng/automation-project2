from typing import List
from pydantic import Field, validator
from ....models import FrozenBaseModel
from ...models import SubscribeResponse, SubscribeRequest


# candlestick.{time_frame}.{instrument_name}
class SubscribeCandlestickInstrumentRequestParams(FrozenBaseModel):
    channels: List[str] = Field(...)


class SubscribeCandlestickInstrumentRequest(SubscribeRequest):
    params: SubscribeCandlestickInstrumentRequestParams = Field(...)


class CandlestickInstrumentDetail(FrozenBaseModel):
    t: str = Field(description="Start time of candlestick (Unix timestamp)")
    o: str = Field(description="Open")
    h: str = Field(description="High")
    l: str = Field(description="Low")
    c: str = Field(description="Close")
    v: str = Field(description="Volume")


class SubscribeCandlestickInstrumentResponseResult(FrozenBaseModel):
    instrument_name: str = Field(description="e.g BTCUSD-PERP")
    interval: str = Field(description="The period (e.g. M5)")
    channel: str = "candlestick"
    subscription: str = Field()
    data: List[CandlestickInstrumentDetail] = Field()

    @validator("subscription")
    def subscription_match(cls, v, values):
        expect = f"candlestick.{values['interval']}.{values['instrument_name']}"
        assert v == expect, f"subscription expect:[{expect}] actual:[{v}]!"
        return v

    @validator("channel")
    def channel_match(cls, v):
        assert v == "candlestick", f"channel expect:[candlestick] actual:[{v}]!"
        return v


class SubscribeCandlestickInstrumentResponse(SubscribeResponse):
    result: SubscribeCandlestickInstrumentResponseResult = Field(default=None)
