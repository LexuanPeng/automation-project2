from typing import List, Optional

from cdc.qa.apis.exchange_oex.models import (
    ExchangeRequestParams,
    ExchangeResponse,
    ExchangeSignedRequest,
    FrozenBaseModel,
)
from pydantic import Field, validator


class PositionDetail(FrozenBaseModel):
    account_id: str = Field(description="Account id")
    quantity: str = Field(description="position size")
    cost: str = Field(description="Position cost")
    open_pos_cost: str = Field(description="Open position cost")
    open_position_pnl: str = Field(description="Profit and loss for the open position")
    session_pnl: str = Field(description="Profit and loss in the current trading session")
    update_timestamp_ms: int = Field(description="Updated time (Unix timestamp)")
    instrument_name: str = Field(description="Position instrument name")
    type: str = Field(description="e.g. Perpetual Swap")


# private/get-positions
class GetPositionsRequestParams(ExchangeRequestParams):
    instrument_name: Optional[str] = Field(default=None, description="e.g. BTC_USDT, ETH_CRO, etc.")


class GetPositionsRequestBody(ExchangeSignedRequest):
    method: str = "private/get-positions"
    params: GetPositionsRequestParams = Field()


class GetPositionsResult(FrozenBaseModel):
    data: List[PositionDetail] = Field()


class GetPositionsResponse(ExchangeResponse):
    result: GetPositionsResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/get-positions"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/close-position
class ClosePositionRequestParams(ExchangeRequestParams):
    instrument_name: str = Field(description="e.g. BTC_USDT, ETH_CRO, etc.")
    type: str = Field(description="order type LIMIT or MARKET")
    price: Optional[str] = Field(default=None, description="For LIMIT orders only")


class ClosePositionRequestBody(ExchangeSignedRequest):
    method: str = "private/close-position"
    params: ClosePositionRequestParams = Field()


class ClosePositionResponseResult(FrozenBaseModel):
    order_id: int = Field(description="Order ID")
    client_oid: str = Field(description="Client Order ID")


class ClosePositionResponse(ExchangeResponse):
    result: ClosePositionResponseResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/close-position"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v
