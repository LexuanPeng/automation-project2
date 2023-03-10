from dataclasses import dataclass, field

from cdc.qa.apis.common.services.ws_service import WsService


@dataclass(frozen=True)
class ExchangeWsService(WsService):
    _api_key: str = field(default="")
    _secret_key: str = field(default="")
