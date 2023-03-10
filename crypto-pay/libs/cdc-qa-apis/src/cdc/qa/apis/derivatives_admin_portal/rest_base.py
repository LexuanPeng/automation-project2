from dataclasses import dataclass, field
from urllib.parse import urlparse, urlunparse

import requests
from cdc.qa.apis.common.models.rest_api import RestApi
from cdc.qa.apis.common.services.rest_service import RestService


@dataclass(frozen=True)
class AdminPortalRestApi(RestApi):
    headers: dict = field(init=False, default_factory=lambda: {"Content-Type": "application/json"})


@dataclass(frozen=True)
class AdminPortalRestService(RestService):
    host: str = field()
    session: requests.Session = field(default_factory=requests.Session)

    def _parse_host(self, shard_name: str):
        parsed_url = urlparse(self.host)
        new_path = f"/{shard_name}{parsed_url.path}"
        # <scheme>://<netloc>/<path>;<params>?<query>#<fragment>
        return urlunparse(
            (
                parsed_url.scheme,
                parsed_url.netloc,
                new_path,
                parsed_url.params,
                parsed_url.query,
                parsed_url.fragment,
            )
        )

    def _get_netloc(self):
        parsed_url = urlparse(self.host)
        return parsed_url.netloc
