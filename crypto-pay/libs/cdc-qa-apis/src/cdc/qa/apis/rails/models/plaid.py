from datetime import datetime

from cdc.qa.apis.rails import RailsResponse
from cdc.qa.apis.rails.models import FrozenBaseModel

from pydantic import Field


# LinkTokensCreate
class LinkTokensCreateRequestData(FrozenBaseModel):
    redirect_url: str = Field("https://st.mona.co/magic/plaid/setup")


class LinkTokensCreateResponse(RailsResponse):
    class LinkToken(FrozenBaseModel):
        expiration: datetime
        link_token: str
        request_id: str

    link_token: LinkToken = Field()
