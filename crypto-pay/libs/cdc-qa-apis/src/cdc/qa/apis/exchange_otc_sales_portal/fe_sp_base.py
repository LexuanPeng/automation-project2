from dataclasses import dataclass, field

import requests
from cdc.qa.apis.common.models.rest_api import RestApi
from cdc.qa.apis.common.services.rest_service import RestService


@dataclass(frozen=True)
class SalesPortalApi(RestApi):
    headers: dict = field(init=False, default_factory=lambda: {"Content-Type": "application/json"})
    token: str = field(default="")
    on_behalf_account: str = field(default=None)

    def __post_init__(self):
        self.headers["token"] = self.token
        if self.on_behalf_account:
            self.headers["on-behalf-account"] = self.on_behalf_account


@dataclass(frozen=True)
class SalesPortalRestService(RestService):
    host: str = field()
    session: requests.Session = field(default_factory=requests.Session)
    token: str = field(default="")
