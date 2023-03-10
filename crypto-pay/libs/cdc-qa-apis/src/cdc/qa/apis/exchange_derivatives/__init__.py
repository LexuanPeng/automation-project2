from dataclasses import dataclass, field, InitVar

from .rest import DerivativesRestServices
from .ws import DerivativesWsServices


@dataclass(frozen=True)
class DerivativesApi:
    api_key: InitVar[str] = field()
    secret_key: InitVar[str] = field()

    rest: DerivativesRestServices = field(init=False)
    ws: DerivativesWsServices = field(init=False)

    def __post_init__(self, api_key, secret_key):
        object.__setattr__(self, "rest", DerivativesRestServices(api_key=api_key, secret_key=secret_key))
        object.__setattr__(self, "ws", DerivativesWsServices(api_key=api_key, secret_key=secret_key))
