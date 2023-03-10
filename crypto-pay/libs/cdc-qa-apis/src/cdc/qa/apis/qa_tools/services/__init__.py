from dataclasses import dataclass, field

import requests

from cdc.qa.apis.common.models.rest_api import RestApi
from cdc.qa.apis.common.services.rest_service import RestService


@dataclass(frozen=True)
class QAToolRestApi(RestApi):
    headers: dict = field(init=False, default_factory=lambda: {"Content-Type": "application/json"})
    log_filters = ["x_csrf_token", "token", "secret_key", "password", "2fa", "2fa_code", "otp_secret"]


@dataclass(frozen=True)
class QAToolRestService(RestService):
    host: str = field()

    api_key: str = field(default="")
    secret_key: str = field(default="")
    session: requests.Session = field(default_factory=requests.Session)
