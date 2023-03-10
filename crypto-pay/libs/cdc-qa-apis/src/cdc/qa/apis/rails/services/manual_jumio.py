from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.rails.data.jumio import DocumentType
from cdc.qa.apis.rails.models import RailsRestApi, RailsRestService
from cdc.qa.apis.rails.models.manual_jumio import (
    ManualJumioCreateRequestData,
    ManualJumioCreateResponse,
    ManualJumioNewRequestParams,
    ManualJumioNewResponse,
    UploadUrls,
)


class ManualJumioCreateApi(RailsRestApi):
    """Submit changes for the manual Jumio."""

    path = "manual_jumio/create"
    method = HttpMethods.POST
    request_data_type = ManualJumioCreateRequestData
    response_type = ManualJumioCreateResponse


class ManualJumioNewApi(RailsRestApi):
    """Get jumio upload pics urls."""

    path = "manual_jumio/new"
    method = HttpMethods.GET
    request_params_type = ManualJumioNewRequestParams
    response_type = ManualJumioNewResponse


class ManualJumioService(RailsRestService):
    def create(self, country_code: str, document_type: DocumentType) -> ManualJumioCreateResponse:
        api = ManualJumioCreateApi(host=self.host, _session=self.session)
        data = ManualJumioCreateRequestData(country_code=country_code, document_type=document_type).dict(
            exclude_none=True
        )

        response = api.call(data=data)
        return ManualJumioCreateResponse.parse_raw(b=response.content)

    def new(self, country_code: str) -> ManualJumioNewResponse:
        api = ManualJumioNewApi(host=self.host, _session=self.session)
        data = ManualJumioNewRequestParams(country_code=country_code).dict(exclude_none=True)

        response = api.call(data=data)
        return ManualJumioNewResponse.parse_raw(b=response.content)

    def get_upload_jumio_pic_urls(self, country_code: str) -> UploadUrls:
        return self.new(country_code).upload_urls
