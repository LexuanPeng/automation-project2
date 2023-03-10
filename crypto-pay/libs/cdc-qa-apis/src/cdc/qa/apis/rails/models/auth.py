from . import FrozenBaseModel, RailsResponse
from pydantic import Field
from .common import User


class OAuthTokenRequestData(FrozenBaseModel):
    terms_of_service_accepted: bool = True
    grant_type: str = "password"
    client_id: str = Field()
    client_secret: str = Field()
    username: str = Field()
    password: str = Field()


class OAuthTokenResponse(RailsResponse):
    access_token: str = Field()
    token_type: str = Field()
    created_at: int = Field()
    user: User = Field()
