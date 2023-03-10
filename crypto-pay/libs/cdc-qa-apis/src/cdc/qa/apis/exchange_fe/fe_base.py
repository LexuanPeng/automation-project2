from dataclasses import dataclass, field

import requests
from cdc.qa.apis.common.models.rest_api import RestApi
from cdc.qa.apis.common.services.rest_service import RestService


@dataclass(frozen=True)
class FeExchangeApi(RestApi):
    headers: dict = field(init=False, default_factory=lambda: {"Content-Type": "application/json"})
    exchange_token: str = field(default="")

    def __post_init__(self):
        self.headers["exchange-token"] = self.exchange_token


@dataclass(frozen=True)
class FeExchangeRestService(RestService):
    host: str = field()
    session: requests.Session = field(default_factory=requests.Session)
    exchange_token: str = field(default="")
