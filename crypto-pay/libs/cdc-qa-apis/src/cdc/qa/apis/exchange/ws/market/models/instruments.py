from decimal import Decimal
from typing import List, Optional
from pydantic import Field, validator
from ....models import FrozenBaseModel
from ...models import SubscribeResponse, SubscribeRequest

"""
include websocket API:
book.{instrument_name}.{depth}
ticker.{instrument_name}
trade.{instrument_name}
candlestick.{interval}.{instrument_name}
"""


# book.{instrument_name}.{depth}
class SubscribeBookInstrumentDepthRequestParams(FrozenBaseModel):
    channels: List[str] = Field(...)


class SubscribeBookInstrumentDepthRequest(SubscribeRequest):
    params: SubscribeBookInstrumentDepthRequestParams = Field(...)


class BookInstrumentDepthDetail(FrozenBaseModel):
    bids: List[List] = Field(description="Updated time (Unix timestamp)")
    asks: List[List] = Field(description="Value of the Mark Price")
    t: int = Field(description="Timestamp of the data")


class SubscribeBookInstrumentDepthResponseResult(FrozenBaseModel):
    instrument_name: str = Field(description="e.g BTC_USD")
    channel: str = "book"
    depth: int = Field(description="Price level")
    subscription: str = Field()
    data: List[BookInstrumentDepthDetail] = Field()

    @validator("channel")
    def channel_match(cls, v):
        assert v == "book", f"channel expect:[book] actual:[{v}]!"
        return v

    @validator("subscription")
    def subscription_match(cls, v, values):
        expect = f"book.{values['instrument_name']}.{values['depth']}"
        assert v == expect, f"subscription expect:[{expect}] actual:[{v}]!"
        return v


class SubscribeBookInstrumentDepthResponse(SubscribeResponse):
    result: Optional[SubscribeBookInstrumentDepthResponseResult] = Field(default=None)


# ticket.{instrument_name}
class SubscribeTickerInstrumentRequestParams(FrozenBaseModel):
    channels: List[str] = Field(...)


class SubscribeTickerInstrumentRequest(SubscribeRequest):
    params: SubscribeTickerInstrumentRequestParams = Field(...)


class TickerInstrumentDataDetail(FrozenBaseModel):
    h: Decimal = Field(description="Price of the 24h highest trade")
    lowerest_trade: Decimal = Field(
        description="Price of the 24h lowest trade, null if there weren't any trades", alias="l"
    )
    a: Decimal = Field(description="The price of the latest trade, null if there weren't any trades")
    i: str = Field(description="Instrument name")
    v: Decimal = Field(description="The total 24h traded volume")
    vv: Decimal = Field(description="The total 24h traded volume value (in USD)")
    oi: Optional[Decimal] = Field(description="The open interest")
    c: Decimal = Field(default=None, description="24-hour price change, null if there weren't any trades")
    b: Decimal = Field(default=None, description="The current best bid price, null if there aren't any bids")
    bs: Decimal = Field(default=None, description="The current best bid size, null if there aren't any bids")
    k: Decimal = Field(default=None, description="The current best ask price, null if there aren't any asks")
    ks: Decimal = Field(default=None, description="The current best ask size, null if there aren't any asks")
    t: int = Field(description="Timestamp of the data")


class SubscribeTickerInstrumentResponseResult(FrozenBaseModel):
    instrument_name: str = Field(description="e.g BTC_USD")
    channel: str = Field(description="Subscribed channel name")
    subscription: str = Field(description="subscribe subscription name")
    data: List[TickerInstrumentDataDetail] = Field()

    @validator("channel")
    def channel_match(cls, v):
        assert v == "ticker", f"channel expect:[ticker] actual:[{v}]!"
        return v

    @validator("subscription")
    def subscription_match(cls, v, values):
        expect = f"ticker.{values['instrument_name']}"
        assert v == expect, f"subscription expect:[{expect}] actual:[{v}]!"
        return v


class SubscribeTickerInstrumentResponse(SubscribeResponse):
    result: Optional[SubscribeTickerInstrumentResponseResult] = Field(default=None)


# trade.{instrument_name}
class SubscribeTradeInstrumentRequestParams(FrozenBaseModel):
    channels: List[str] = Field(...)


class SubscribeTradeInstrumentRequest(SubscribeRequest):
    params: SubscribeTradeInstrumentRequestParams = Field(...)


class TradeInstrumentDataDetail(FrozenBaseModel):
    p: Decimal = Field(description="Trade price")
    q: Decimal = Field(description="Trade quantity")
    s: str = Field(description='Side ("buy" or "sell")')
    d: int = Field(description="Trade ID")
    t: int = Field(description="Trade timestamp")
    dataTime: Optional[int] = Field(description="Reserved. Can be ignored")
    i: str = Field(description="instrument name")


class SubscribeTradeInstrumentResponseResult(FrozenBaseModel):
    instrument_name: str = Field("e.g. ETH_USDT")
    channel: str = Field(description="Subscribed channel name")
    subscription: str = Field(description="subscribe subscription name")
    data: List[TradeInstrumentDataDetail] = Field()

    @validator("channel")
    def channel_match(cls, v):
        assert v == "trade", f"channel expect:[trade] actual:[{v}]!"
        return v

    @validator("subscription")
    def subscription_match(cls, v, values):
        expect = f"trade.{values['instrument_name']}"
        assert v == expect, f"subscription expect:[{expect}] actual:[{v}]!"
        return v


class SubscribeTradeInstrumentResponse(SubscribeResponse):
    result: Optional[SubscribeTradeInstrumentResponseResult] = Field(default=None)


# candlestick.{intervel}.{instrument_name}
class SubscribeCandlestickIntervelInstrumentRequestParams(FrozenBaseModel):
    channels: List[str] = Field(...)


class SubscribeCandlestickIntervelInstrumentRequest(SubscribeRequest):
    params: SubscribeCandlestickIntervelInstrumentRequestParams = Field(...)


class CandlestickIntervelInstrumentDataDetail(FrozenBaseModel):
    o: Decimal = Field(description="Open")
    h: Decimal = Field(description="High")
    l: Decimal = Field(description="Low", alias="l")
    c: Decimal = Field(description="Close")
    v: Decimal = Field(description="Volume")
    t: int = Field(description="End time of candlestick (Unix timestamp)")
    ut: int = Field(description="Update time of candlestick (Unix timestamp)")


class SubscribeCandlestickIntervelInstrumentResponseResult(FrozenBaseModel):
    instrument_name: str = Field(description="instrument_name")
    interval: str = Field()
    channel: str = Field(description="Subscribed channel name")
    subscription: str = Field(description="subscribe subscription name")
    data: List[CandlestickIntervelInstrumentDataDetail] = Field()

    @validator("channel")
    def channel_match(cls, v):
        assert v == "candlestick", f"channel expect:[candlestick] actual:[{v}]!"
        return v

    @validator("subscription")
    def subscription_match(cls, v, values):
        expect = f"candlestick.{values['interval']}.{values['instrument_name']}"
        assert v == expect, f"subscription expect:[{expect}] actual:[{v}]!"
        return v


class SubscribeCandlestickIntervelInstrumentResponse(SubscribeResponse):
    result: Optional[SubscribeCandlestickIntervelInstrumentResponseResult] = Field(default=None)
