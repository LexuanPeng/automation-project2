from typing import List
from pydantic import Field, validator
from ....models import FrozenBaseModel
from ...models import SubscribeResponse, SubscribeRequest


class SubscribeMarkInstrumentRequestParams(FrozenBaseModel):
    channels: List[str] = Field(...)


class SubscribeMarkInstrumentRequest(SubscribeRequest):
    params: SubscribeMarkInstrumentRequestParams = Field(...)


class MarkInstrumentDetail(FrozenBaseModel):
    t: int = Field(description="Updated time (Unix timestamp)")
    v: str = Field(description="Value of the Mark Price")


class SubscribeMarkInstrumentResponseResult(FrozenBaseModel):
    instrument_name: str = Field(description="e.g BTCUSD-PERP")
    channel: str = "mark"
    subscription: str = Field()
    data: List[MarkInstrumentDetail] = Field()

    @validator("subscription")
    def subscription_match(cls, v, values):
        expect = f"mark.{values['instrument_name']}"
        assert v == expect, f"subscription expect:[{expect}] actual:[{v}]!"
        return v

    @validator("channel")
    def channel_match(cls, v):
        assert v == "mark", f"channel expect:[mark] actual:[{v}]!"
        return v


class SubscribeMarkInstrumentResponse(SubscribeResponse):
    result: SubscribeMarkInstrumentResponseResult = Field(default=None)
