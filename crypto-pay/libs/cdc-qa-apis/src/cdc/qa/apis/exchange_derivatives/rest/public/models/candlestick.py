from typing import List, Optional

from cdc.qa.apis.exchange_derivatives.models import DerivativesResponse, FrozenBaseModel
from pydantic import Field, validator


class GetCandlestickRequestParams(FrozenBaseModel):
    instrument_name: str = Field(description="e.g. BTC_USDT, ETH_CRO, etc.")
    timeframe: str = Field(default="M5", description="period, default is 5m")


class CandlestickDetail(FrozenBaseModel):
    t: int = Field(description="End time of candlestick (Unix timestamp)")
    o: float = Field(description="Open price")
    h: float = Field(description="High price")
    l: float = Field(description="Low price")
    c: float = Field(description="Close price")
    v: float = Field(description="Volume price")


class GetCandlestickResult(FrozenBaseModel):
    instrument_name: str = Field(description="e.g. BTC_USDT, ETH_CRO, etc.")
    interval: str = Field(description="Interval value for each candlestick results")
    data: Optional[List[CandlestickDetail]] = Field(default=None)


class GetCandlestickResponse(DerivativesResponse):
    result: GetCandlestickResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "public/get-candlestick"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v
