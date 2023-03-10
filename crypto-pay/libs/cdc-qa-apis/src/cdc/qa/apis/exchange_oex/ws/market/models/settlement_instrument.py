from typing import List
from pydantic import Field, validator
from ....models import FrozenBaseModel
from ...models import SubscribeResponse, SubscribeRequest


class SubscribeSettlementInstrumentRequestParams(FrozenBaseModel):
    channels: List[str] = Field(...)


class SubscribeSettlementInstrumentRequest(SubscribeRequest):
    params: SubscribeSettlementInstrumentRequestParams = Field(...)


class SettlementInstrumentDetail(FrozenBaseModel):
    t: int = Field(description="Updated time (Unix timestamp)")
    v: str = Field(description="Value of the Settlement")


class SubscribeSettlementInstrumentResponseResult(FrozenBaseModel):
    instrument_name: str = Field(description="e.g BTCUSD-220930")
    channel: str = "settlement"
    subscription: str = Field()
    data: List[SettlementInstrumentDetail] = Field()

    @validator("subscription")
    def subscription_match(cls, v, values):
        instrument_name = values.get("instrument_name")
        expect = ["settlement"]
        if instrument_name is not None:
            expect.append(f"settlement.{instrument_name}")
        assert v in expect, f"subscription expect in:[{expect}] actual:[{v}]!"
        return v

    @validator("channel")
    def channel_match(cls, v):
        assert v == "settlement", f"channel expect:[settlement] actual:[{v}]!"
        return v


class SubscribeSettlementInstrumentResponse(SubscribeResponse):
    result: SubscribeSettlementInstrumentResponseResult = Field(default=None)
