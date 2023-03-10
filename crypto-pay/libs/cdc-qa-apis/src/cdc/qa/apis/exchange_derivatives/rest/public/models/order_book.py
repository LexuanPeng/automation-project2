from typing import List, Optional

from cdc.qa.apis.exchange_derivatives.models import DerivativesResponse, FrozenBaseModel
from pydantic import Field, validator


class GetBookRequestParams(FrozenBaseModel):
    instrument_name: str = Field(description="e.g. BTC_USDT, ETH_CRO, etc.")
    depth: Optional[int] = Field(default=None, description="Number of bids and asks to return (up to 50)", ge=0, le=50)


class GetBookResultData(FrozenBaseModel):
    bids: List[List[str]] = Field(description="Bids array: [0] = Price, [1] = Quantity, [2] = Number of Orders")
    asks: List[List[str]] = Field(description="Asks array: [0] = Price, [1] = Quantity, [2] = Number of Orders")
    t: int = Field(description="Timestamp of the data")


class GetBookResult(FrozenBaseModel):
    instrument_name: str = Field()
    depth: int = Field()
    data: Optional[List[GetBookResultData]] = Field(default=None)


class GetBookResponse(DerivativesResponse):
    result: GetBookResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "public/get-book"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v
