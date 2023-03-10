from cdc.qa.apis.rails import RailsResponse
from cdc.qa.apis.rails.models.common import Account

from pydantic import Field


# AccountShow
class AccountShowResponse(RailsResponse):
    account: Account = Field()
