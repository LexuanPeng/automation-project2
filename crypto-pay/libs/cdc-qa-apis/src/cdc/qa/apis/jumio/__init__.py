from dataclasses import dataclass, field

import requests
from cdc.qa.apis.jumio.services.file import FileService


@dataclass(frozen=True)
class JumioApi:
    _host: str = field(default="https://manual-jumio-staginga.s3-ap-southeast-1.amazonaws.com")
    _session: requests.Session = field(default_factory=requests.Session)

    file: FileService = field(init=False)

    def __post_init__(self):
        self._session.hooks["response"].append(lambda r, *args, **kwargs: r.raise_for_status())

        services = {
            "file": FileService,
        }

        for k, v in services.items():
            object.__setattr__(self, k, v(host=self._host, session=self._session))
