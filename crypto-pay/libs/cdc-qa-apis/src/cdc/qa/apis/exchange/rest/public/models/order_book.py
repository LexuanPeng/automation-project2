from decimal import Decimal
from typing import List, Optional

from cdc.qa.apis.exchange.models import ExchangeResponse, FrozenBaseModel
from pydantic import Field


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
    instrument_name: str = Field()
    depth: int = Field()
    data: Optional[List[GetBookResultData]] = Field(default=None)


class GetBookResponse(ExchangeResponse):
    result: GetBookResult = Field()
