from dataclasses import InitVar, dataclass, field

import requests

from .services.data_manager import DataManagerService
from .services.exchange import ExchangeService
from .services.ops import OpsService


@dataclass(frozen=True)
class QAToolsApiServices:
    api_key: InitVar[str] = field()
    secret_key: InitVar[str] = field()

    host: str = field(default="https://oqsta-meta.3ona.co/api/")
    session: requests.Session = field(default_factory=requests.Session)

    data_manager: DataManagerService = field(init=False)
    exchange: ExchangeService = field(init=False)
    ops: OpsService = field(init=False)

    def __post_init__(self, api_key, secret_key):
        services = {
            "data_manager": DataManagerService,
            "exchange": ExchangeService,
            "ops": OpsService,
        }

        for k, v in services.items():
            object.__setattr__(self, k, v(host=self.host, session=self.session, api_key=api_key, secret_key=secret_key))
