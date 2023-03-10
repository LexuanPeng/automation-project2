from pydantic import Field, validator
from typing import List, Optional
from decimal import Decimal
from ....models import FrozenBaseModel, ExchangeRequest, ExchangeResponse
from ...models import SubscribeResponse, SubscribeRequest


class SubscribeUserTradeInstrumentRequestParams(FrozenBaseModel):
    channels: List[str] = Field(...)


class SubscribeUserTradeInstrumentRequest(SubscribeRequest):
    params: SubscribeUserTradeInstrumentRequestParams = Field(...)


class SubscribeUserTradeInstrumentData(FrozenBaseModel):
    side: str = Field(description="BUY or SELL")
    instrument_name: str = Field(description="e.g. ETH_CRO, BTC_USDT")
    fee: Decimal = Field(description="Trade fee")
    trade_id: str = Field(description="Trade id")
    create_time: int = Field(description="Trade creation time")
    traded_price: Decimal = Field(description="Executed trade price")
    traded_quantity: Decimal = Field(description="Executed trade quantity")
    fee_currency: str = Field(description="Currency used for the fees (e.g. CRO)")
    order_id: str = Field(description="Order ID")


class SubscribeUserTradeInstrumentResponseResult(FrozenBaseModel):
    instrument_name: str = Field(description="e.g. ETH_CRO, BTC_USDT")
    subscription: str = Field(description="user.trade.{instrument_name} -- even in the all case")
    channel: str = Field(description="user.trade")
    data: List[SubscribeUserTradeInstrumentData] = Field()

    @validator("subscription")
    def subscription_match(cls, v, values):
        expect = f"user.trade.{values['instrument_name']}"
        assert v == expect, f"subscription expect:[{expect}] actual:[{v}]!"
        return v

    @validator("channel")
    def channel_match(cls, v):
        assert v == "user.trade", f"channel expect:[user.trade] actual:[{v}]!"
        return v


class SubscribeUserTradeInstrumentResponse(SubscribeResponse):
    result: SubscribeUserTradeInstrumentResponseResult = Field()


# private/get-trades
class PrivateGetTradesRequestParams(FrozenBaseModel):
    instrument_name: Optional[str] = Field(description="e.g. ETH_CRO, BTC_USDT. Omit for 'all'")
    start_ts: Optional[int] = Field(
        description="Start timestamp (milliseconds since the Unix epoch) - defaults to 24 hours ago"
    )
    end_ts: Optional[int] = Field(description="End timestamp (milliseconds since the Unix epoch) - defaults to 'now'")
    page_size: Optional[int] = Field(description="Page size (Default: 20, max: 200)")
    page: Optional[int] = Field(description="Page number (0-based)")


class PrivateGetTradesRequest(ExchangeRequest):
    method: str = "private/get-trades"
    params: PrivateGetTradesRequestParams = Field(description="Get Trades Request Params")


class TradeDetailInfo(FrozenBaseModel):
    side: str = Field(description="BUY, SELL")
    instrument_name: str = Field(description="e.g. ETH_CRO, BTC_USDT")
    fee: Decimal = Field(description="Trade fee")
    trade_id: str = Field(description="Trade ID")
    create_time: int = Field(description="Trade creation time")
    traded_price: Decimal = Field(description="Executed trade price")
    traded_quantity: Decimal = Field(description="Executed trade quantity")
    fee_currency: str = Field(description="Currency used for the fees (e.g. CRO)")
    order_id: str = Field(description="Order ID")
    client_oid: str = Field(description="Client Order ID")
    liquidity_indicator: str = Field(description="TAKER or MAKER")


class PrivateGetTradesResult(FrozenBaseModel):
    trade_list: List[TradeDetailInfo] = Field(description="trade list")


class PrivateGetTradesResponse(ExchangeResponse):
    result: PrivateGetTradesResult = Field(description="Get Trade Response")
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/get-trades"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v
