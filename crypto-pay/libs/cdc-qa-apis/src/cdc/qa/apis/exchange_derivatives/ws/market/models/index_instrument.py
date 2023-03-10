from typing import List
from pydantic import Field, validator
from ....models import FrozenBaseModel
from ...models import SubscribeResponse, SubscribeRequest


class SubscribeIndexInstrumentRequestParams(FrozenBaseModel):
    channels: List[str] = Field(...)


class SubscribeIndexInstrumentRequest(SubscribeRequest):
    params: SubscribeIndexInstrumentRequestParams = Field(...)


class IndexInstrumentDetail(FrozenBaseModel):
    t: int = Field(description="Updated time (Unix timestamp)")
    v: str = Field(description="Value of the Index Price")


class SubscribeIndexInstrumentResponseResult(FrozenBaseModel):
    instrument_name: str = Field(description="e.g BTCUSD-PERP")
    channel: str = "index"
    subscription: str = Field()
    data: List[IndexInstrumentDetail] = Field()

    @validator("subscription")
    def subscription_match(cls, v, values):
        expect = f"index.{values['instrument_name']}"
        assert v == expect, f"subscription expect:[{expect}] actual:[{v}]!"
        return v

    @validator("channel")
    def channel_match(cls, v):
        assert v == "index", f"channel expect:[index] actual:[{v}]!"
        return v


class SubscribeIndexInstrumentResponse(SubscribeResponse):
    result: SubscribeIndexInstrumentResponseResult = Field(default=None)
