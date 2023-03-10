from typing import Optional

from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.rails.models.address import (
    AddressUpdateRequestData,
    AddressUpdateResponse,
    Address,
    ResidentialAddressCreateRequestData,
    ResidentialAddressUpdateResponse,
    AddressProofUpdateRequestData,
    AddressProofUpdateResponse,
)

from ..models import RailsRestApi, RailsRestService


class AddressShowApi(RailsRestApi):
    """Show user account address."""

    path = "address/show"
    method = HttpMethods.GET
    response_type = AddressUpdateResponse


class AddressProofUpdateApi(RailsRestApi):
    """Show user account address."""

    path = "address/proof/update"
    method = HttpMethods.POST
    request_data_type = AddressProofUpdateRequestData
    response_type = AddressProofUpdateResponse


class AddressUpdateApi(RailsRestApi):
    """Update user account address."""

    path = "address/update"
    method = HttpMethods.POST
    request_data_type = AddressUpdateRequestData
    response_type = AddressUpdateResponse


class ResidentialAddressCreateApi(RailsRestApi):
    """Create residential address. (for AUS users)."""

    path = "residential_address/create"
    method = HttpMethods.POST
    request_data_type = ResidentialAddressCreateRequestData
    response_type = ResidentialAddressUpdateResponse


class AddressService(RailsRestService):
    def update(
        self,
        address_1: str,
        address_2: str,
        city: str,
        country: str,
        postcode: str,
        zip_code: str,
        state_code: Optional[str] = None,
        province: Optional[str] = None,
    ) -> AddressUpdateResponse:
        api = AddressUpdateApi(host=self.host, _session=self.session)
        data = AddressUpdateRequestData(
            address=Address(
                address_1=address_1,
                address_2=address_2,
                city=city,
                country=country,
                postcode=postcode,
                zip_code=zip_code,
                state_code=state_code,
                province=province,
            ),
        ).dict(exclude_none=True)

        response = api.call(json=data)
        return AddressUpdateResponse.parse_raw(b=response.content)

    def residential_address_create(
        self,
        address_1: str,
        country: str,
        postcode: str,
        state: str,
        town: str,
        address_2: Optional[str] = None,
    ) -> ResidentialAddressUpdateResponse:
        api = ResidentialAddressCreateApi(host=self.host, _session=self.session)
        data = ResidentialAddressCreateRequestData(
            address_line_1=address_1,
            address_line_2=address_2,
            country=country,
            postcode=postcode,
            state=state,
            town=town,
        ).dict(exclude_none=True)

        response = api.call(json=data)
        return ResidentialAddressUpdateResponse.parse_raw(b=response.content)

    def show(self) -> AddressUpdateResponse:
        api = AddressShowApi(host=self.host, _session=self.session)

        response = api.call()
        return AddressUpdateResponse.parse_raw(b=response.content)

    def proof_update(self, submit_for: str = "card_application") -> AddressProofUpdateResponse:
        api = AddressProofUpdateApi(host=self.host, _session=self.session)
        data = AddressProofUpdateRequestData(submit_for=submit_for).dict(exclude_none=True)

        response = api.call(json=data)
        return AddressProofUpdateResponse.parse_raw(b=response.content)
