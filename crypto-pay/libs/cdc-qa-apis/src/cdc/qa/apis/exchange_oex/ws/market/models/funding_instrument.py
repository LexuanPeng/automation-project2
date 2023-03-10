from typing import List
from pydantic import Field, validator
from ....models import FrozenBaseModel
from ...models import SubscribeResponse, SubscribeRequest


class SubscribeFundingInstrumentRequestParams(FrozenBaseModel):
    channels: List[str] = Field(...)


class SubscribeFundingInstrumentRequest(SubscribeRequest):
    params: SubscribeFundingInstrumentRequestParams = Field(...)


class FundingInstrumentDetail(FrozenBaseModel):
    t: int = Field(description="Updated time (Unix timestamp)")
    v: str = Field(description="Value of the Funding Price")


class SubscribeFundingInstrumentResponseResult(FrozenBaseModel):
    instrument_name: str = Field(description="e.g BTCUSD-PERP")
    channel: str = "funding"
    subscription: str = Field()
    data: List[FundingInstrumentDetail] = Field()

    @validator("subscription")
    def subscription_match(cls, v, values):
        expect = f"funding.{values['instrument_name']}"
        assert v == expect, f"subscription expect:[{expect}] actual:[{v}]!"
        return v

    @validator("channel")
    def channel_match(cls, v):
        assert v == "funding", f"channel expect:[funding] actual:[{v}]!"
        return v


class SubscribeFundingInstrumentResponse(SubscribeResponse):
    result: SubscribeFundingInstrumentResponseResult = Field(default=None)
