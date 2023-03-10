from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.plaid.models import PlaidRestApi, PlaidRestService
from cdc.qa.apis.plaid.models.link import ItemCreateRequestData, ItemCreateResponse


class ItemCreateApi(PlaidRestApi):
    path = "/link/item/create"
    method = HttpMethods.POST
    request_data_type = ItemCreateRequestData
    response_type = ItemCreateResponse


class LinkService(PlaidRestService):
    def item_create(self, link_token: str) -> ItemCreateResponse:
        """Create Plaid link item, default `Citi Bank`."""

        api = ItemCreateApi(host=self.host, _session=self.session)
        data = ItemCreateRequestData(link_token=link_token).dict(exclude_none=True)

        response = api.call(json=data)
        return ItemCreateResponse.parse_raw(b=response.content)
