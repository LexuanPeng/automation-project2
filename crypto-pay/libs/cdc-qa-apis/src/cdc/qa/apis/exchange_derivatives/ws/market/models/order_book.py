from typing import List
from pydantic import Field, validator
from ....models import FrozenBaseModel
from ...models import SubscribeResponse, SubscribeRequest


class SubscribeBookInstrumentRequestParams(FrozenBaseModel):
    channels: List[str] = Field(...)


class SubscribeBookInstrumentRequest(SubscribeRequest):
    params: SubscribeBookInstrumentRequestParams = Field(...)


class BookInstrumentDetail(FrozenBaseModel):
    asks: List[List[str]] = Field(description="asks list")
    bids: List[List[str]] = Field(description="bids list")
    t: int = Field(description="time stamp")
    tt: int
    u: int


class SubscribeBookInstrumentResponseResult(FrozenBaseModel):
    instrument_name: str = Field(description="e.g BTCUSD-PERP")
    channel: str = "book"
    depth: int = Field(description="Number of bids and asks to return")
    subscription: str = Field()
    data: List[BookInstrumentDetail] = Field()

    @validator("subscription")
    def subscription_match(cls, v, values):
        depth = values.get("depth")
        instrument_name = values.get("instrument_name")
        expect = [f"book.{instrument_name}.{depth}"]
        if depth == 50:
            expect.append(f"book.{instrument_name}")

        assert v in expect, f"subscription expect in:[{expect}] actual:[{v}]!"
        return v

    @validator("channel")
    def channel_match(cls, v):
        assert v == "book", f"channel expect:[book] actual:[{v}]!"
        return v


class SubscribeBookInstrumentResponse(SubscribeResponse):
    result: SubscribeBookInstrumentResponseResult = Field(default=None)
