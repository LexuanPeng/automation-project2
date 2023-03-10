from typing import List, Optional
from pydantic import Field, validator

from ...models import SubscribeResponse, SubscribeRequest
from ....models import FrozenBaseModel, DerivativesRequest, DerivativesResponse


class PositionDetail(FrozenBaseModel):
    account_id: str = Field(description="instrument name")
    quantity: str = Field(description="instrument quantity")
    liquidation_price: Optional[str] = Field(description="liquidation price")
    session_unrealized_pnl: Optional[str] = Field(description="unrealized pnl")
    cost: str = Field(description="position cost")
    open_position_pnl: str = Field(description="pnl for the open position")
    open_pos_cost: str = Field(description="open position cost")
    session_pnl: str = Field(description="pnl in the trading session")
    pos_initial_margin: Optional[str] = Field(description="initial margin")
    pos_maintenance_margin: Optional[str] = Field(description="maintenance margin")
    market_value: Optional[str] = Field(description="market value")
    mark_price: Optional[str] = Field(description="mark price")
    effective_leverage: Optional[str] = Field(description="leverage")
    target_leverage: Optional[str] = Field(description="leverage")
    update_timestamp_ms: int = Field(description="Update time(Unix timestamp)")
    type: str = Field(description="type")
    instrument_name: str = Field(description="instrument name")


class SubscribeUserPositionsRequestParams(FrozenBaseModel):
    channels: List[str] = ["user.positions"]


class SubscribeUserPositionsRequest(SubscribeRequest):
    params: SubscribeUserPositionsRequestParams = SubscribeUserPositionsRequestParams()


class SubscribeUserPositionsResponseResult(FrozenBaseModel):
    channel: str = "user.positions"
    subscription: str = "user.positions"
    data: List[PositionDetail] = Field()

    @validator("channel")
    def channel_match(cls, v):
        assert v == "user.positions", f"channel expect:[user.positions] actual:[{v}]!"
        return v

    @validator("subscription")
    def subscription_match(cls, v):
        assert v == "user.positions", f"subscription expect:[user.positions] actual:[{v}]!"
        return v


class SubscribeUserPositionsResponse(SubscribeResponse):
    result: SubscribeUserPositionsResponseResult = Field(default=None)


# private/get-positions
class PrivateGetPositionsRequestParams(FrozenBaseModel):
    instrument_name: Optional[str] = Field(default=None, description="e.g. BTC_USDT, ETH_CRO, etc.")


class PrivateGetPositionsRequest(DerivativesRequest):
    method: str = "private/get-positions"
    params: PrivateGetPositionsRequestParams = Field()


class PrivateGetPositionsResponseResult(FrozenBaseModel):
    data: List[PositionDetail] = Field()


class PrivateGetPositionsResponse(DerivativesResponse):
    result: PrivateGetPositionsResponseResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/get-positions"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/close-position
class PrivateClosePositionRequestParams(FrozenBaseModel):
    instrument_name: str = Field(description="e.g. BTC_USDT, ETH_CRO, etc.")
    type: str = Field(description="order type LIMIT or MARKET")
    price: Optional[str] = Field(default=None, description="For LIMIT orders only")


class PrivateClosePositionRequest(DerivativesRequest):
    method: str = "private/close-position"
    params: PrivateClosePositionRequestParams = Field()


class PrivateClosePositionResponseResult(FrozenBaseModel):
    order_id: int = Field(description="Order ID")
    client_oid: str = Field(description="Client Order ID")


class PrivateClosePositionResponse(DerivativesResponse):
    result: PrivateClosePositionResponseResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/close-position"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v
