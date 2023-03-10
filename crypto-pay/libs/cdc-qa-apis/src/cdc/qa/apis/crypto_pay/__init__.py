from dataclasses import dataclass, field

import requests

from cdc.qa.apis.crypto_pay.services.payment import PaymentService
from cdc.qa.apis.crypto_pay.services.token import TokenService


@dataclass(frozen=True)
class CryptoPayApi:
    _session: requests.Session = field(default_factory=requests.Session)

    token: TokenService = field(init=False)
    payment: PaymentService = field(init=False)

    def __post_init__(self):
        # self._session.hooks["response"].append(lambda r, *args, **kwargs: r.raise_for_status())

        services = {"token": TokenService, "payment": PaymentService}

        for k, v in services.items():
            object.__setattr__(self, k, v(session=self._session))
