from dataclasses import InitVar, dataclass, field

from .ws_base import ExchangeWebSocketClient
from .user import ExchangeWsUserServices
from .market import ExchangeWsMarketServices


__all__ = [
    "ExchangeWebSocketClient",
    "ExchangeWsServices",
    "ExchangeWsUserServices",
    "ExchangeWsMarketServices",
]


@dataclass(frozen=True)
class ExchangeWsServices:
    api_key: InitVar[str] = field()
    secret_key: InitVar[str] = field()
    host: InitVar[str] = field(default="wss://uat-stream.3ona.co/v2/")

    user: ExchangeWsUserServices = field(init=False)
    market: ExchangeWsMarketServices = field(init=False)

    def __post_init__(self, api_key, secret_key, host):
        object.__setattr__(self, "user", ExchangeWsUserServices(api_key=api_key, secret_key=secret_key, host=host))
        object.__setattr__(self, "market", ExchangeWsMarketServices(host=host))
