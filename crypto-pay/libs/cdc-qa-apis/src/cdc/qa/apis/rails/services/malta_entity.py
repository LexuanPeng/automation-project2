from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.rails.models import RailsRestApi, RailsRestService
from cdc.qa.apis.rails.models.malta_entity import (
    AddressResponse,
    AddressRequestData,
    MaltaAddressProofResponse,
    MaltaAddressProofRequestData,
    MaltaRiskAssessmentsRequestData,
    MaltaRiskAssessmentsResponse,
    MaltaRiskAssessmentsAnswerResponse,
)


class MaltaEntityApi(RailsRestApi):
    """Submit address for Malta entity."""

    path = "malta_entity/addresses"
    method = HttpMethods.POST
    request_data_type = AddressRequestData
    response_type = AddressResponse


class MaltaEntityAddressProofApi(RailsRestApi):
    path = "malta_entity/addresses/address_proof"
    method = HttpMethods.POST
    request_data_type = MaltaAddressProofRequestData
    response_type = MaltaAddressProofResponse


class MaltaRiskAssessmentsAnswerApi(RailsRestApi):
    path = "risk_assessments?status=unanswered"
    method = HttpMethods.GET
    response_type = MaltaRiskAssessmentsAnswerResponse


class MaltaRiskAssessmentsApi(RailsRestApi):
    path = "risk_assessments"
    method = HttpMethods.POST
    request_data_type = MaltaRiskAssessmentsRequestData
    response_type = MaltaRiskAssessmentsResponse


class MaltaEntityService(RailsRestService):
    def addresses(
        self,
        address_line_1: str,
        address_line_2,
        address_line_3,
        country: str,
        postcode: str,
        state: str,
        town: str,
    ) -> AddressResponse:
        api = MaltaEntityApi(host=self.host, _session=self.session)
        data = AddressRequestData(
            address_line_1=address_line_1,
            address_line_2=address_line_2,
            address_line_3=address_line_3,
            country=country,
            postcode=postcode,
            state=state,
            town=town,
        ).dict(exclude_none=True)

        response = api.call(data=data)
        return AddressResponse.parse_raw(b=response.content)

    def upload_proof(self) -> MaltaAddressProofResponse:
        api = MaltaEntityAddressProofApi(host=self.host, _session=self.session)
        data = MaltaAddressProofRequestData().dict(exclude_none=True)

        response = api.call(data=data)
        return MaltaAddressProofResponse.parse_raw(b=response.content)

    def risk_assessments(self, choice: str, answer_id: str) -> MaltaRiskAssessmentsResponse:
        api = MaltaRiskAssessmentsApi(host=self.host, _session=self.session)
        data = MaltaRiskAssessmentsRequestData(choice=choice, id=answer_id).dict(exclude_none=True)

        response = api.call(data=data)
        return MaltaRiskAssessmentsResponse.parse_raw(b=response.content)

    def risk_assessments_answers(self) -> MaltaRiskAssessmentsAnswerResponse:
        api = MaltaRiskAssessmentsAnswerApi(host=self.host, _session=self.session)

        response = api.call()
        return MaltaRiskAssessmentsAnswerResponse.parse_raw(b=response.content)
