from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.rails.models import RailsRestApi, RailsRestService
from cdc.qa.apis.rails.models.balances import BalancesTotalResponse


class BalancesTotalApi(RailsRestApi):
    """Show account total balance"""

    path = "balances/total"
    method = HttpMethods.GET
    response_type = BalancesTotalResponse


class BalancesService(RailsRestService):
    def total(self) -> BalancesTotalResponse:
        api = BalancesTotalApi(host=self.host, _session=self.session)

        response = api.call()
        return BalancesTotalResponse.parse_raw(b=response.content)
