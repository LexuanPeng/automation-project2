from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.rails.models import RailsRestApi, RailsRestService
from cdc.qa.apis.rails.models.account import AccountShowResponse


class AccountShowApi(RailsRestApi):
    """Show account information."""

    path = "account/show"
    method = HttpMethods.GET
    response_type = AccountShowResponse


class AccountService(RailsRestService):
    def show(self) -> AccountShowResponse:
        api = AccountShowApi(host=self.host, _session=self.session)

        response = api.call()
        return AccountShowResponse.parse_raw(b=response.content)

    def get_user_id(self) -> int:
        return self.show().account.id
