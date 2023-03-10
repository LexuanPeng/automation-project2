from typing import List
from pydantic import Field, validator
from ....models import FrozenBaseModel
from ...models import SubscribeResponse, SubscribeRequest


# ticker.{instrument_name}
class SubscribeTickerInstrumentRequestParams(FrozenBaseModel):
    channels: List[str] = Field(...)


class SubscribeTickerInstrumentRequest(SubscribeRequest):
    params: SubscribeTickerInstrumentRequestParams = Field(...)


class TickerInstrumentDetail(FrozenBaseModel):
    h: str = Field(default=None, description="Price of the 24h highest trade")
    l: str = Field(default=None, description="Price of the 24h lowest trade, null if there weren't any trades")
    a: str = Field(default=None, description="The price of the latest trade, null if there weren't any trades")
    i: str = Field(description="Instrument name")
    v: str = Field(default=None, description="The total 24h traded volume")
    vv: str = Field(default=None, description="The total 24h traded volume value (in USD)")
    oi: str = Field(default=None, description="The open interest")
    c: str = Field(default=None, description="24-hour price change, null if there weren't any trades")
    b: str = Field(default=None, description="The current best bid price, null if there aren't any bids")
    k: str = Field(default=None, description="The current best ask price, null if there aren't any asks")
    t: int = Field(description="Trade timestamp")


class SubscribeTickerInstrumentResponseResult(FrozenBaseModel):
    instrument_name: str = Field(description="e.g BTCUSD-PERP")
    channel: str = "ticker"
    subscription: str = Field()
    data: List[TickerInstrumentDetail] = Field()

    @validator("subscription")
    def subscription_match(cls, v, values):
        instrument_name = values.get("instrument_name")
        expect = ["ticker"]
        if instrument_name is not None:
            expect.append(f"ticker.{instrument_name}")
        assert v in expect, f"subscription expect in:[{expect}] actual:[{v}]!"
        return v

    @validator("channel")
    def channel_match(cls, v):
        assert v == "ticker", f"channel expect:[ticker] actual:[{v}]!"
        return v


class SubscribeTickerInstrumentResponse(SubscribeResponse):
    result: SubscribeTickerInstrumentResponseResult = Field(default=None)
