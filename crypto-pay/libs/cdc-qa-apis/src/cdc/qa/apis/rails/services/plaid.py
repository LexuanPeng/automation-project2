from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.rails.models import RailsRestApi, RailsRestService
from cdc.qa.apis.rails.models.plaid import LinkTokensCreateResponse, LinkTokensCreateRequestData


class LinkTokensCreateApi(RailsRestApi):
    """Get Plaid link tokens for ACH bank."""

    path = "plaid/link_tokens/create"
    method = HttpMethods.POST
    response_type = LinkTokensCreateResponse


class PlaidService(RailsRestService):
    def link_tokens_create(self) -> LinkTokensCreateResponse:
        api = LinkTokensCreateApi(host=self.host, _session=self.session)
        data = LinkTokensCreateRequestData().dict(exclude_none=True)

        response = api.call(data=data)
        return LinkTokensCreateResponse.parse_raw(b=response.content)
