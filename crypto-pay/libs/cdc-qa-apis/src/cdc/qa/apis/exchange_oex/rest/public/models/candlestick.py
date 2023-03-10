from typing import List, Optional

from cdc.qa.apis.exchange_oex.models import ExchangeResponse, FrozenBaseModel
from pydantic import Field, validator


class GetCandlestickRequestParams(FrozenBaseModel):
    instrument_name: str = Field(description="e.g. BTC_USDT, ETH_CRO, etc.")
    timeframe: Optional[str] = Field(description="The period value as show below. Default is M1.")
    count: Optional[int] = Field(default="25", description="Default is 25")
    start_ts: Optional[int] = Field(description="Default timestamp is 1 day ago (Unix timestamp)")
    end_ts: Optional[int] = Field(description="Default timestamp is current time (Unix timestamp)")


class GetCandlestickResultData(FrozenBaseModel):
    t: int = Field(description="Start time of candlestick (Unix timestamp)")
    o: str = Field(description="Open price")
    h: str = Field(description="High price")
    l: str = Field(description="Low price")
    c: str = Field(description="Close price")
    v: str = Field(description="Volume price")


class GetCandlestickResult(FrozenBaseModel):
    instrument_name: str = Field(description="e.g. BTC_USDT, ETH_CRO, etc.")
    interval: str = Field(description="The period (e.g. M5)")
    data: Optional[List[GetCandlestickResultData]] = Field(default=None)


class GetCandlestickResponse(ExchangeResponse):
    result: GetCandlestickResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "public/get-candlestick"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v
