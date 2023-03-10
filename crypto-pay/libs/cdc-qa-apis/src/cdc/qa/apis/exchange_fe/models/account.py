from ..fe_models import FeExchangeRequest, FeExchangeResponse, FrozenBaseModel
from pydantic import Field
from typing import Optional


class CreateMarginAccountRequest(FeExchangeRequest):
    pass


class CreateMarginAccountDataDetail(FrozenBaseModel):
    category: str = Field(description="category: margin")


class CreateMarginAccountResponse(FeExchangeResponse):
    data: Optional[CreateMarginAccountDataDetail] = Field(description="Create Margin Account Response")
