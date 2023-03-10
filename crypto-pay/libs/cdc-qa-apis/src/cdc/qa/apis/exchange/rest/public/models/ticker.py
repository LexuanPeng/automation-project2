from typing import List, Optional
from decimal import Decimal

from cdc.qa.apis.exchange.models import ExchangeResponse, FrozenBaseModel
from pydantic import Field


class GetTickerRequestParams(FrozenBaseModel):
    instrument_name: Optional[str] = Field(description="e.g. BTC_USDT, ETH_CRO, etc.")


class GetTickerResultData(FrozenBaseModel):
    h: Decimal = Field(default=None, description="Price of the 24h highest trade")
    l: Decimal = Field(default=None, description="Price of the 24h lowest trade, null if there weren't any trades")
    a: Decimal = Field(default=None, description="The price of the latest trade, null if there weren't any trades")
    i: str = Field(description="Instrument Name, e.g. BTC_USDT, ETH_CRO, etc.")
    v: Decimal = Field(default=None, description="The total 24h traded volume")
    vv: Decimal = Field(default=None, description="The total 24h traded volume value (in USD)")
    oi: Decimal = Field(default=None, description="The open interest")
    c: Decimal = Field(default=None, description="24-hour price change, null if there weren't any trades")
    b: Decimal = Field(default=None, description="The current best ask price, null if there aren't any bids")
    k: Decimal = Field(default=None, description="The current best ask price, null if there aren't any asks")
    t: int = Field(default=None, description="Timestamp of the data")


class GetTickerResult(FrozenBaseModel):
    data: List[GetTickerResultData] = Field()


class GetTickerResponse(ExchangeResponse):
    result: GetTickerResult = Field()


class GetAllTickersResult(FrozenBaseModel):
    data: Optional[List[GetTickerResultData]] = Field()


class GetAllTickersResponse(ExchangeResponse):
    result: GetAllTickersResult = Field()
