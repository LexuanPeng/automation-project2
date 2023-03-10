from typing import Optional
from cdc.qa.apis.rails import RailsResponse
from cdc.qa.apis.rails.models import FrozenBaseModel, RailsEncryptedPasscodeRequest
from cdc.qa.apis.rails.models.common import Balance, TransferUser

from pydantic import Field

# --------------------------------- TransferCreate --------------------------------- #


class Transfer(FrozenBaseModel):
    id: int
    from_user: TransferUser
    to_user: TransferUser
    amount: Balance
    native_amount: Balance
    note: Optional[str]
    status: str
    sending: bool
    referral_url: str
    created_at: str
    updated_at: str


class TransferCreateRequestData(RailsEncryptedPasscodeRequest):
    to_name: str
    to_phone: str
    amount: Optional[str]
    currency: str
    otp: Optional[str]
    phone_otp: Optional[str]
    native_amount: Optional[str]


class TransferCreateResponse(RailsResponse):
    transfer: Transfer = Field()
