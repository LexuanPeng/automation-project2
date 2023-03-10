from dataclasses import InitVar, dataclass, field

from .ws_base import DerivativesWebSocketClient
from .user import DerivativesWsUserServices
from .market import DerivativesWsMarketServices


__all__ = [
    "DerivativesWebSocketClient",
    "DerivativesWsServices",
    "DerivativesWsUserServices",
    "DerivativesWsMarketServices",
]


@dataclass(frozen=True)
class DerivativesWsServices:
    api_key: InitVar[str] = field()
    secret_key: InitVar[str] = field()
    host: InitVar[str] = field(default="wss://uat-deriv-stream.3ona.co/v1/")

    user: DerivativesWsUserServices = field(init=False)
    market: DerivativesWsMarketServices = field(init=False)

    def __post_init__(self, api_key, secret_key, host):
        object.__setattr__(self, "user", DerivativesWsUserServices(api_key=api_key, secret_key=secret_key, host=host))
        object.__setattr__(self, "market", DerivativesWsMarketServices(host=host))
