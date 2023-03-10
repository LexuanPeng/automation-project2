from decimal import Decimal
from typing import List, Optional

from cdc.qa.apis.exchange_oex.models import ExchangeResponse, FrozenBaseModel
from pydantic import Field, validator


class GetBookRequestParams(FrozenBaseModel):
    instrument_name: str = Field(description="e.g. BTC_USDT, ETH_CRO, etc.")
    depth: Optional[int] = Field(
        default=None, description="Number of bids and asks to return (up to 150)", ge=0, le=150
    )


class GetBookResultData(FrozenBaseModel):
    bids: List[List[Decimal]] = Field(description="Bids array: [0] = Price, [1] = Quantity, [2] = Number of Orders")
    asks: List[List[Decimal]] = Field(description="Asks array: [0] = Price, [1] = Quantity, [2] = Number of Orders")
    t: int = Field(description="Timestamp of the data")


class GetBookResult(FrozenBaseModel):
    instrument_name: str = Field("e.g. BTCUSD-PERP")
    depth: int = Field("Number of bids and asks to return (up to 50)")
    data: Optional[List[GetBookResultData]] = Field(default=None)


class GetBookResponse(ExchangeResponse):
    result: GetBookResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "public/get-book"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v
