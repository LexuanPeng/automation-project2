from typing import List, Optional

from cdc.qa.apis.exchange_oex.models import ExchangeResponse, FrozenBaseModel
from pydantic import Field, validator


class GetInsuranceRequestParams(FrozenBaseModel):
    instrument_name: str = Field(description="e.g. BTC_USDT, ETH_CRO, etc.")
    count: Optional[int] = Field(default=None, description="Default is 25")
    start_ts: Optional[int] = Field(default=None, description="Default timestamp is 1 day ago (Unix timestamp)")
    end_ts: Optional[int] = Field(default=None, description="Default timestamp is current time (Unix timestamp)")


class InsuranceDetail(FrozenBaseModel):
    v: str = Field(description="value")
    t: int = Field(description="Timestamp of the data")


class GetInsuranceResult(FrozenBaseModel):
    instrument_name: str = Field(description="e.g. USD_Stable_Coin")
    data: Optional[List[InsuranceDetail]] = Field()


class GetInsuranceResponse(ExchangeResponse):
    result: GetInsuranceResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "public/get-insurance"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v
