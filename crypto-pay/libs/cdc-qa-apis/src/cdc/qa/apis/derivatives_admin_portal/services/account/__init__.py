from dataclasses import dataclass, field

import requests

from .account_service import AccountService
from .position_service import PositionService


@dataclass(frozen=True)
class AccountServices:
    host: str = field()
    session: requests.Session = field(default_factory=requests.Session)

    account_service: AccountService = field(init=False)
    position_service: PositionService = field(init=False)

    def __post_init__(self):
        services = {
            "account_service": AccountService,
            "position_service": PositionService,
        }

        for k, v in services.items():
            object.__setattr__(self, k, v(host=self.host, session=self.session))
