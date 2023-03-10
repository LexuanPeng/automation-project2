from typing import Optional, List

from cdc.qa.apis.rails import RailsResponse
from cdc.qa.apis.rails.models import FrozenBaseModel

from pydantic import Field


class PayStringEligibleResponse(FrozenBaseModel):
    ok: bool
    eligible: bool


class RegisterPayStringRequestData(FrozenBaseModel):
    acct_part: str = Field()


class Currencies(FrozenBaseModel):
    currencies: Optional[List[str]]
    enabled: bool
    network: str


class PayID(FrozenBaseModel):
    user_uuid: str
    full_address: str
    acct_part: str
    currencies: List[Currencies]
    status: str


class PayStringResponse(RailsResponse):
    pay_id: PayID = Field()


class UpdatePayStringRequest(FrozenBaseModel):
    currencies: List[Currencies]
