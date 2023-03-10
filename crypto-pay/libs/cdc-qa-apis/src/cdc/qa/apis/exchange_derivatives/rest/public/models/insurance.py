from decimal import Decimal
from typing import List, Optional

from cdc.qa.apis.exchange_derivatives.models import DerivativesResponse, FrozenBaseModel
from pydantic import Field, validator


class GetInsuranceRequestParams(FrozenBaseModel):
    instrument_name: str = Field(description="e.g. BTC_USDT, ETH_CRO, etc.")
    count: int = Field(default=None, description="")
    start_ts: int = Field(default=None, description="start timestamp")
    end_ts: int = Field(default=None, description="end timestamp")


class InsuranceDetail(FrozenBaseModel):
    v: Decimal = Field(description="value")
    t: int = Field(description="Timestamp of the data")


class GetInsuranceResult(FrozenBaseModel):
    instrument_name: str = Field()
    data: Optional[List[InsuranceDetail]] = Field()


class GetInsuranceResponse(DerivativesResponse):
    result: GetInsuranceResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "public/get-insurance"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v
