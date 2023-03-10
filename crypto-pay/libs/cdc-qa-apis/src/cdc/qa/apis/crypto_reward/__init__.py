from dataclasses import dataclass, field

import requests
from cdc.qa.apis.crypto_reward.services.feature import FeatureStatusService
from cdc.qa.apis.crypto_reward.services.auth import AuthService


@dataclass(frozen=True)
class CryptoRewardApi:
    _host: str = field(default="https://asta-crypto-reward-v2-api.3ona.co/api/")
    _session: requests.Session = field(default_factory=requests.Session)

    feature_status: FeatureStatusService = field(init=False)
    auth: AuthService = field(init=False)

    def __post_init__(self):
        self._session.hooks["response"].append(lambda r, *args, **kwargs: r.raise_for_status())

        services = {
            "feature_status": FeatureStatusService,
            "auth": AuthService,
        }

        for k, v in services.items():
            object.__setattr__(self, k, v(host=self._host, session=self._session))
