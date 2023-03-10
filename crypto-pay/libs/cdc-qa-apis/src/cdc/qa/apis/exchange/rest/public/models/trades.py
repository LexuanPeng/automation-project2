from typing import List, Optional

from cdc.qa.apis.exchange.models import ExchangeResponse, FrozenBaseModel
from pydantic import Field


class GetTradesRequestParams(FrozenBaseModel):
    instrument_name: Optional[str] = Field(description="e.g. BTC_USDT, ETH_CRO, etc.")
    size: Optional[int]


class GetTradesResultData(FrozenBaseModel):
    s: str = Field(description="Side ('buy' or 'sell')")
    p: str = Field(description="Trade price")
    q: str = Field(description="Trade quantity")
    t: int = Field(description="Trade timestamp")
    i: str = Field(description="Instrument name")


class GetTradesResult(FrozenBaseModel):
    data: List[GetTradesResultData] = Field()


class GetTradesResponse(ExchangeResponse):
    result: GetTradesResult = Field()
