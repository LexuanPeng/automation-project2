from dataclasses import dataclass, field, InitVar

from .rest import ExchangeRestServices
from .ws import ExchangeWsServices


@dataclass(frozen=True)
class ExchangeApi:
    api_key: InitVar[str] = field()
    secret_key: InitVar[str] = field()

    rest: ExchangeRestServices = field(init=False)
    ws: ExchangeWsServices = field(init=False)

    def __post_init__(self, api_key, secret_key):
        object.__setattr__(self, "rest", ExchangeRestServices(api_key=api_key, secret_key=secret_key))
        object.__setattr__(self, "ws", ExchangeWsServices(api_key=api_key, secret_key=secret_key))
