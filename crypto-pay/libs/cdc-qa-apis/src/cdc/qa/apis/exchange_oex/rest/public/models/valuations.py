from typing import List, Optional

from cdc.qa.apis.exchange_oex.models import ExchangeResponse, FrozenBaseModel
from pydantic import Field, validator


class GetValuationsRequestParams(FrozenBaseModel):
    instrument_name: str = Field(description="e.g. BTC_USDT-PERP or BTC_USDT Index, etc.")
    valuation_type: str = Field(description="e.g. index_price, funding_hist, mark_price, settlement_price")
    count: Optional[int] = Field(default=None, description="Default is 25")
    start_ts: Optional[int] = Field(
        default=None,
        description="Default timestamp is 30 days ago for funding_hist, "
        "and 1 day ago for other valuation_type (Unix timestamp)",
    )
    end_ts: Optional[int] = Field(default=None, description="Default timestamp is current time (Unix timestamp)")


class GetValuationsDetail(FrozenBaseModel):
    v: str = Field(description="value of Index price, Mark price, funding_rate or settlement_price")
    t: int = Field(description="Timestamp of the data")


class GetValuationsResult(FrozenBaseModel):
    instrument_name: str = Field()
    data: Optional[List[GetValuationsDetail]] = Field()


class GetValuationsResponse(ExchangeResponse):
    result: GetValuationsResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "public/get-valuations"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v
