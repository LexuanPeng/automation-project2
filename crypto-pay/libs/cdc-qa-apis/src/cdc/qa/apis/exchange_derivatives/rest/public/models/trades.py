from typing import List

from cdc.qa.apis.exchange_derivatives.models import DerivativesResponse, FrozenBaseModel
from pydantic import Field, validator


class GetTradesRequestParams(FrozenBaseModel):
    instrument_name: str = Field(description="e.g. BTCUSD-PERP")
    count: int = Field(default=None, description="Default is 25")


class TradeDetail(FrozenBaseModel):
    s: str = Field(description="Side ('buy' or 'sell')")
    p: str = Field(description="Trade price")
    q: str = Field(description="Trade quantity")
    t: int = Field(description="Trade timestamp")
    i: str = Field(description="Instrument name")


class GetTradesResult(FrozenBaseModel):
    data: List[TradeDetail] = Field()


class GetTradesResponse(DerivativesResponse):
    result: GetTradesResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "public/get-trades"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v
