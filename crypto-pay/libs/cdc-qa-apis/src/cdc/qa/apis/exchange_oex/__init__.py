from dataclasses import InitVar, dataclass, field

from .rest import OneExchangeRestServices
from .ws import OneExchangeWsServices


@dataclass(frozen=True)
class OneExchangeApi:
    api_key: InitVar[str] = field()
    secret_key: InitVar[str] = field()

    rest: OneExchangeRestServices = field(init=False)
    ws: OneExchangeWsServices = field(init=False)

    def __post_init__(self, api_key, secret_key):
        object.__setattr__(self, "rest", OneExchangeRestServices(api_key=api_key, secret_key=secret_key))
        object.__setattr__(self, "ws", OneExchangeWsServices(api_key=api_key, secret_key=secret_key))
