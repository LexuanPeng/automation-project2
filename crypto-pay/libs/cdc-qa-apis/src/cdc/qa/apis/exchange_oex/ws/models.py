from ..models import FrozenBaseModel, ExchangeResponse, ExchangeRequest
from pydantic import Field, validator
from typing import Optional


class RespondHeartbeatRequest(FrozenBaseModel):
    id: int = Field(
        default=None,
        description="Request Identifier. Response message will contain the same id",
        ge=0,
        le=9_223_372_036_854_775_807,
    )
    method: str = "public/respond-heartbeat"


class SubscribeRequest(ExchangeRequest):
    method: str = "subscribe"


class SubscribeResponseResult(FrozenBaseModel):
    channel: str = Field(description="Subscribed channel name")
    subscription: str = Field(description="subscribe subscription name")


class SubscribeResponse(ExchangeResponse):
    method: str = "subscribe"
    result: Optional[SubscribeResponseResult] = Field()

    @validator("method")
    def method_match(cls, v):
        if v != "subscribe":
            raise ValueError("method do not match [subscribe]")
        return v
