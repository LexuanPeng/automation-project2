from dataclasses import dataclass, field

import requests

from .refdata_service import RefDataService
from .glob_settl_service import GlobSettlService


@dataclass(frozen=True)
class GlobalServices:
    host: str = field()
    session: requests.Session = field(default_factory=requests.Session)

    refdata_service: RefDataService = field(init=False)
    glob_settl_service: GlobSettlService = field(init=False)

    def __post_init__(self):
        services = {
            "refdata_service": RefDataService,
            "glob_settl_service": GlobSettlService,
        }

        for k, v in services.items():
            object.__setattr__(self, k, v(host=self.host, session=self.session))
