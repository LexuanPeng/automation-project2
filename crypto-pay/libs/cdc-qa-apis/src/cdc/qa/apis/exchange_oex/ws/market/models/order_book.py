from typing import List, Optional
from pydantic import Field, validator
from ....models import FrozenBaseModel
from ...models import SubscribeResponse, SubscribeRequest


# book.{instrument_name} / book.{instrument_name}.{depth}
class SubscribeBookInstrumentRequestParams(FrozenBaseModel):
    """
    If book_subscription_type is SNAPSHOT_AND_UPDATE, allowed values on book_update_frequency is 5 and 10 (default).
    If book_subscription_type is SNAPSHOT, allowed values on book_update_frequency is 10, 50 (default).
    """

    channels: List[str] = Field(...)
    book_subscription_type: Optional[str] = Field(
        description="Allowed values: SNAPSHOT (default) or SNAPSHOT_AND_UPDATE (new beta feature)"
    )
    book_update_frequency: Optional[int] = Field(description="In milliseconds")


class SubscribeBookInstrumentRequest(SubscribeRequest):
    params: SubscribeBookInstrumentRequestParams = Field(...)


class AsksBidsDetail(FrozenBaseModel):
    asks: List[List[str]] = Field(description="asks list")
    bids: List[List[str]] = Field(description="bids list")


class BookInstrumentDetail(FrozenBaseModel):
    asks: Optional[List[List[str]]] = Field(description="asks list")
    bids: Optional[List[List[str]]] = Field(description="bids list")
    t: int = Field(description="Epoch millis of last book update")
    tt: int = Field(description="Epoch millis of message publish")
    u: int = Field(description="Update sequence")
    pu: Optional[int] = Field(description="Previous update sequence")
    cs: int = Field(description="check sum")
    update: Optional[AsksBidsDetail] = Field(description="bids and asks")


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
        expect.append("book.update")

        assert v in expect, f"subscription expect in:[{expect}] actual:[{v}]!"
        return v

    @validator("channel")
    def channel_match(cls, v):
        assert v in ["book", "book.update"], f"channel expect:[book, book.update] actual:[{v}]!"
        return v


class SubscribeBookInstrumentResponse(SubscribeResponse):
    result: SubscribeBookInstrumentResponseResult = Field(default=None)
