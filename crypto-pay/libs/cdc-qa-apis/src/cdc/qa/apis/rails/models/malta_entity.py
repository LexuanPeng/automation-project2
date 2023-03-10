from cdc.qa.apis.rails.models import FrozenBaseModel, RailsResponse

from pydantic import Field

from cdc.qa.apis.rails.models.address import AddressProofUpdateRequestData
from cdc.qa.apis.rails.models.common import RiskAssessments, RiskAssessmentsAnswer


# addresses
class AddressRequestData(FrozenBaseModel):
    address_line_1: str = Field()
    address_line_2: str = Field()
    address_line_3: str = Field()
    country: str = Field()
    postcode: int = Field()
    state: str = Field()
    town: str = Field()


class AddressResponse(RailsResponse):
    class Address(FrozenBaseModel):
        id: str
        status: str
        address_line_1: str
        address_line_2: str
        address_line_3: str
        town: str
        state: str
        postcode: int
        country: str

    address: Address = Field()


class MaltaAddressProofRequestData(AddressProofUpdateRequestData):
    pass


class MaltaAddressProofResponse(AddressResponse):
    pass


class MaltaRiskAssessmentsRequestData(RiskAssessments):
    pass


class MaltaRiskAssessmentsResponse(RailsResponse):
    pass


class MaltaRiskAssessmentsAnswerResponse(RiskAssessmentsAnswer, RailsResponse):
    pass
