from cdc.qa.apis.rails import RailsResponse
from cdc.qa.apis.rails.models import FrozenBaseModel
from cdc.qa.apis.rails.models.common import Balance

from pydantic import Field


class BalancesTotalResponse(RailsResponse):
    class Balances(FrozenBaseModel):
        native_currency: str
        total_balance: Balance
        price_change: Balance
        percent_change: str

    balances: Balances = Field()
