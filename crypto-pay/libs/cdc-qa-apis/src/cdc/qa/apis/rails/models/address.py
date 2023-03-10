import uuid
from datetime import datetime
from typing import Optional

from cdc.qa.apis.rails import RailsResponse
from cdc.qa.apis.rails.models import FrozenBaseModel
from cdc.qa.apis.rails.models.common import Address

from pydantic import Field


# AddressUpdate
class AddressUpdateRequestData(FrozenBaseModel):
    address: Address


class AddressUpdateResponse(RailsResponse):
    address: Address
    inject_http_status_code: Optional[int]


# ResidentialAddressCreate
class ResidentialAddressCreateRequestData(FrozenBaseModel):
    address_line_1: str
    address_line_2: str
    country: str
    postcode: str
    state: str
    town: str


class ResidentialAddressUpdateResponse(RailsResponse):
    class ResidentialAddress(FrozenBaseModel):
        id: str
        user_uuid: str
        address_line_1: str
        address_line_2: str = Field(default="")
        town: str
        state: str
        postcode: str
        country: str
        created_at: datetime
        updated_at: datetime
        address_line_3: Optional[str]

    residential_address: ResidentialAddress = Field()


class AddressProofUpdateRequestData(FrozenBaseModel):
    submit_for: Optional[str]
    proof_scan_reference: str = Field(default=uuid.uuid4().__str__())


class AddressProofUpdateResponse(RailsResponse):
    class Verification(FrozenBaseModel):
        verification: str

    address_proof: Optional[Verification]
