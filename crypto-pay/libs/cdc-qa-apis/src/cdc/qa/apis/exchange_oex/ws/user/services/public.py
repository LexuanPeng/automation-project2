from typing import List

from ....models import ExchangeRequestParams
from ...ws_base import ExchangeWsService
from ..models.auth import AuthRequest, AuthResponse


class UserPublicService(ExchangeWsService):
    def send_auth(self, system_label: str = None):
        request = AuthRequest(
            api_key=self._api_key,
            secret_key=self._secret_key,
            params=ExchangeRequestParams(system_label=system_label),
        ).json(exclude_none=True)
        self.client.send(request)

    def get_auth_msgs(self, *args, **kwargs) -> List[AuthResponse]:
        return list(map(AuthResponse.parse_raw, self.client.get_messages(method="public/auth", *args, **kwargs)))
