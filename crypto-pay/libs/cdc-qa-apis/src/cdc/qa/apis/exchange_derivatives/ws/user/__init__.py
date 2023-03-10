from dataclasses import InitVar, dataclass, field
from typing import Optional
from urllib.parse import urljoin

from .services.private import UserPrivateService
from ..ws_base import DerivativesWebSocketClient
from .services.public import UserPublicService
from .services.subscribe import UserSubscribeService


@dataclass(frozen=True)
class DerivativesWsUserServices:
    api_key: InitVar[str] = field()
    secret_key: InitVar[str] = field()
    host: InitVar[str] = field(default="wss://dstg-ws-gateway.x.3ona.co/v1/")
    heartbeat_auto_respond: InitVar[bool] = field(default=True)
    heartbeat_save_message: InitVar[bool] = field(default=False)

    _path: str = field(default="user", init=False)
    _client: DerivativesWebSocketClient = field(init=False)

    public: UserPublicService = field(init=False)
    subscribe: UserSubscribeService = field(init=False)
    private: UserPrivateService = field(init=False)

    def __post_init__(self, api_key, secret_key, host, heartbeat_auto_respond, heartbeat_save_message):
        object.__setattr__(
            self,
            "_client",
            DerivativesWebSocketClient(
                host=urljoin(host, self._path),
                heartbeat_auto_respond=heartbeat_auto_respond,
                heartbeat_save_message=heartbeat_save_message,
            ),
        )

        services = {
            "public": UserPublicService,
            "subscribe": UserSubscribeService,
            "private": UserPrivateService,
        }

        for k, v in services.items():
            object.__setattr__(self, k, v(client=self._client, _api_key=api_key, _secret_key=secret_key))

    def connect(self, alias: Optional[str] = None):
        self._client.connect(alias)

    def is_connected(self):
        return self._client.is_connected()

    def disconnect(self):
        self._client.disconnect()

    def clear(self):
        self._client.clear()
