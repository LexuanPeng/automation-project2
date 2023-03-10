from dataclasses import dataclass, field, InitVar

from . import private, public
from .public import PublicServices
from .private import PrivateServices
from .rest_base import DerivativesRestApi, DerivativesRestService

import requests

__all__ = ["DerivativesRestApi", "DerivativesRestService", "public", "private"]


@dataclass(frozen=True)
class DerivativesRestServices:
    api_key: InitVar[str] = field()
    secret_key: InitVar[str] = field()

    host: str = field(default="https://dstg-rest-gateway.x.3ona.co/deriv/v1/")
    session: requests.Session = field(default_factory=requests.Session)

    public: PublicServices = field(init=False)
    private: PrivateServices = field(init=False)

    def __post_init__(self, api_key, secret_key):
        services = {
            "public": PublicServices,
            "private": PrivateServices,
        }

        for k, v in services.items():
            object.__setattr__(self, k, v(host=self.host, session=self.session, api_key=api_key, secret_key=secret_key))
