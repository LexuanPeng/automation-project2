from typing import List

from ...ws_base import DerivativesWsService
from ..models.auth import AuthRequest, AuthResponse
from ..models.instruments import PublicGetInstrumentsRequest, PublicGetInstrumentsResponse


class UserPublicService(DerivativesWsService):
    def send_auth(self):
        request = AuthRequest(api_key=self._api_key, secret_key=self._secret_key).json(exclude_none=True)
        self.client.send(request)

    def get_auth_msgs(self, *args, **kwargs) -> List[AuthResponse]:
        return list(map(AuthResponse.parse_raw, self.client.get_messages(method="public/auth", *args, **kwargs)))

    def send_get_instruments(self):
        request = PublicGetInstrumentsRequest().json(exclude_none=True)
        self.client.send(request)

    def get_get_instruments_msgs(self, *args, **kwargs) -> List[PublicGetInstrumentsResponse]:
        return list(
            map(
                PublicGetInstrumentsResponse.parse_raw,
                self.client.get_messages(method="public/get-instruments", *args, **kwargs),
            )
        )
