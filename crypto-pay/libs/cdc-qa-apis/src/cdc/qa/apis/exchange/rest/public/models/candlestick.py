from typing import List, Optional

from cdc.qa.apis.exchange.models import ExchangeResponse, FrozenBaseModel
from pydantic import Field


class GetCandlestickRequestParams(FrozenBaseModel):
    instrument_name: str = Field(description="e.g. BTC_USDT, ETH_CRO, etc.")
    timeframe: str = Field(default="5m", description="period, default is 5m")


class GetCandlestickResultData(FrozenBaseModel):
    t: int = Field(description="End time of candlestick (Unix timestamp)")
    o: float = Field(description="Open price")
    h: float = Field(description="High price")
    l: float = Field(description="Low price")
    c: float = Field(description="Close price")
    v: float = Field(description="Volume price")


class GetCandlestickResult(FrozenBaseModel):
    instrument_name: str = Field(description="e.g. BTC_USDT, ETH_CRO, etc.")
    interval: str = Field(description="Interval value for each candlestick results")
    data: Optional[List[GetCandlestickResultData]] = Field(default=None)


class GetCandlestickResponse(ExchangeResponse):
    result: GetCandlestickResult = Field()
