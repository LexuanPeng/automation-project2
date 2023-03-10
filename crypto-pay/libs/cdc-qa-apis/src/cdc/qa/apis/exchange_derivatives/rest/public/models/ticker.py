from typing import List
from decimal import Decimal

from cdc.qa.apis.exchange_derivatives.models import DerivativesResponse, FrozenBaseModel
from pydantic import Field, validator


class GetTickersRequestParams(FrozenBaseModel):
    instrument_name: str = Field(default=None, description="e.g. BTC_USDT, ETH_CRO, etc.")


class TickerDetail(FrozenBaseModel):
    i: str = Field(description="Instrument Name, e.g. BTC_USDT, ETH_CRO, etc.")
    b: Decimal = Field(default=None, description="The current best ask price, null if there aren't any bids")
    k: Decimal = Field(default=None, description="The current best ask price, null if there aren't any asks")
    a: Decimal = Field(default=None, description="The price of the latest trade, null if there weren't any trades")
    t: int = Field(default=None, description="Timestamp of the data")
    v: Decimal = Field(default=None, description="The total 24h traded volume")
    h: Decimal = Field(default=None, description="Price of the 24h highest trade")
    l: Decimal = Field(default=None, description="Price of the 24h lowest trade, null if there weren't any trades")
    c: Decimal = Field(default=None, description="24-hour price change, null if there weren't any trades")


class GetTickersResult(FrozenBaseModel):
    data: List[TickerDetail] = Field()


class GetTickersResponse(DerivativesResponse):
    result: GetTickersResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "public/get-tickers"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v
