from dataclasses import dataclass, field

import requests
from oauth2client.service_account import ServiceAccountCredentials
from requests.auth import AuthBase

from cdc.qa.apis.firebase_remote_config.services.config import ConfigService


class BearerAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["Authorization"] = f"Bearer {self.token}"
        return r


@dataclass(frozen=True)
class FirebaseRemoteConfigApi:
    keyfile_dict: dict = field()

    _host: str = field(default="https://firebaseremoteconfig.googleapis.com")
    _session: requests.Session = field(default_factory=requests.Session)

    config: ConfigService = field(init=False)

    def __post_init__(self):
        SCOPES = ["https://www.googleapis.com/auth/firebase.remoteconfig"]
        token = (
            ServiceAccountCredentials.from_json_keyfile_dict(self.keyfile_dict, SCOPES).get_access_token().access_token
        )
        self._session.auth = BearerAuth(token)
        self._session.hooks["response"].append(lambda r, *args, **kwargs: r.raise_for_status())

        services = {
            "config": ConfigService,
        }

        for k, v in services.items():
            object.__setattr__(self, k, v(host=self._host, session=self._session))
