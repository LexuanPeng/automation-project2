import os

from cdc.qa.core import secretsmanager as sm

from cdc.qa.apis.common.models.rest_api import HttpMethods


from ..models import RailsRestApi, RailsRestService, BearerAuth
from ..models.auth import OAuthTokenRequestData, OAuthTokenResponse


class OAuthTokenApi(RailsRestApi):
    """Generate OAuth token for user."""

    path = "oauth/token"
    method = HttpMethods.POST
    request_data_type = OAuthTokenRequestData
    response_type = OAuthTokenResponse


class AuthService(RailsRestService):
    def get_token(self, email: str, magic_token: str) -> OAuthTokenResponse:
        """Generate OAuth token for user."""
        api = OAuthTokenApi(host=self.host, _session=self.session)

        client_id = os.environ.get("OAUTH_CLIENT_ID", None)
        client_secret = os.environ.get("OAUTH_CLIENT_SECRET", None)

        if not client_id or not client_secret:
            se = sm.get_secret_json(self.secret_id)
            client_id = se["OAUTH_CLIENT_ID"]
            client_secret = se["OAUTH_CLIENT_SECRET"]

        data = OAuthTokenRequestData(
            username=email,
            password=magic_token,
            client_id=client_id,
            client_secret=client_secret,
        ).dict(exclude_none=True)

        response = api.call(json=data)
        return OAuthTokenResponse.parse_raw(b=response.content)

    def set_token(self, token: str):
        """Set authentication for this session."""
        self.session.auth = BearerAuth(token)

    def authenticate(self, email: str, magic_token: str) -> str:
        """Generate OAuth token and set authentication for this session."""
        token = self.get_token(email, magic_token).access_token
        self.set_token(token)
        return token
