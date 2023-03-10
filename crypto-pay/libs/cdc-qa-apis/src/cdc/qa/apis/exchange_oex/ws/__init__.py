from dataclasses import InitVar, dataclass, field

from .ws_base import ExchangeWebSocketClient
from .user import OneExchangeWsUserServices
from .market import OneExchangeWsMarketServices


__all__ = [
    "ExchangeWebSocketClient",
    "OneExchangeWsServices",
    "OneExchangeWsUserServices",
    "OneExchangeWsMarketServices",
]


@dataclass(frozen=True)
class OneExchangeWsServices:
    api_key: InitVar[str] = field()
    secret_key: InitVar[str] = field()
    host: InitVar[str] = field(default="wss://uat-stream.3ona.co/v2/")

    user: OneExchangeWsUserServices = field(init=False)
    market: OneExchangeWsMarketServices = field(init=False)

    def __post_init__(self, api_key, secret_key, host):
        object.__setattr__(self, "user", OneExchangeWsUserServices(api_key=api_key, secret_key=secret_key, host=host))
        object.__setattr__(self, "market", OneExchangeWsMarketServices(host=host))
