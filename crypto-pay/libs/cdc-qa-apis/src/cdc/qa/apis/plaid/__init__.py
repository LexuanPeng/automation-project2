from dataclasses import dataclass, field

import requests
from .services.link import LinkService


@dataclass(frozen=True)
class PlaidApi:
    _host: str = field(default="https://sandbox.plaid.com")
    _session: requests.Session = field(default_factory=requests.Session)

    link: LinkService = field(init=False)

    def __post_init__(self):
        self._session.hooks["response"].append(lambda r, *args, **kwargs: r.raise_for_status())

        services = {
            "link": LinkService,
        }

        for k, v in services.items():
            object.__setattr__(self, k, v(host=self._host, session=self._session))
