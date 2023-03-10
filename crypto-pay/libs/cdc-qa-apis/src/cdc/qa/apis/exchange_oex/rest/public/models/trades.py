from typing import List, Optional

from cdc.qa.apis.exchange_oex.models import ExchangeResponse, FrozenBaseModel
from pydantic import Field, validator


class GetTradesRequestParams(FrozenBaseModel):
    instrument_name: str = Field(description="e.g. BTC_USDT, ETH_CRO, etc.")
    count: Optional[int] = Field(description="Default is 25")
    start_ts: Optional[int] = Field(description="Default timestamp is 1 day ago (Unix timestamp)")
    end_ts: Optional[int] = Field(description="Default timestamp is current time (Unix timestamp)")


class GetTradesResultData(FrozenBaseModel):
    s: str = Field(description="Side ('buy' or 'sell')")
    p: str = Field(description="Trade price")
    q: str = Field(description="Trade quantity")
    t: int = Field(description="Trade timestamp")
    i: str = Field(description="Instrument name")
    d: str = Field(description="Trade ID")


class GetTradesResult(FrozenBaseModel):
    data: List[GetTradesResultData] = Field()


class GetTradesResponse(ExchangeResponse):
    result: GetTradesResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "public/get-trades"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v
