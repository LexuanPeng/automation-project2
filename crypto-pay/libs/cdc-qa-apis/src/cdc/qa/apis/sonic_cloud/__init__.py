from dataclasses import dataclass, field, InitVar

import requests

from .models import SonicCloudResponse, SonicCloudError
from .services.appium import AppiumService


@dataclass(frozen=True)
class SonicCloudApi:
    uuid_key: InitVar[str] = field()

    _host: str = field(default="http://10.10.170.20:3000")
    _session: requests.Session = field(default_factory=requests.Session)

    appium: AppiumService = field(init=False)

    def __post_init__(self, uuid_key: str):
        def raise_for_error(_r):
            response = SonicCloudResponse.parse_raw(b=_r.content)
            if not response.code == 2000:
                raise SonicCloudError(f"{response.message=}")

        self._session.hooks["response"].append(lambda r, *args, **kwargs: r.raise_for_status())
        self._session.hooks["response"].append(lambda r, *args, **kwargs: raise_for_error(r))

        self._session.headers.update({"uuid_key": uuid_key})

        services = {
            "appium": AppiumService,
        }

        for k, v in services.items():
            object.__setattr__(self, k, v(host=self._host, session=self._session, uuid_key=uuid_key))

    def close_session(self):
        self._session.close()
