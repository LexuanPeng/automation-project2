from typing import List, Optional

from cdc.qa.apis.exchange_derivatives.models import DerivativesResponse, FrozenBaseModel
from pydantic import Field, validator


class GetValuationsRequestParams(FrozenBaseModel):
    instrument_name: str = Field(description="e.g. BTC_USDT-PERP or BTC_USDT Index, etc.")
    valuation_type: str = Field(description="index_price, funding_rate, mark_price")
    count: int = Field(default=None, description="Return the data row count")
    start_ts: int = Field(default=None, description="start time")
    end_ts: int = Field(default=None, description="end time")


class GetValuationDetail(FrozenBaseModel):
    v: str = Field(description="value of Index price, Mark price or funding_rate")
    t: int = Field(description="Timestamp of the data")


class GetValuationsResult(FrozenBaseModel):
    instrument_name: str = Field()
    data: Optional[List[GetValuationDetail]] = Field()


class GetValuationsResponse(DerivativesResponse):
    result: GetValuationsResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "public/get-valuations"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v
