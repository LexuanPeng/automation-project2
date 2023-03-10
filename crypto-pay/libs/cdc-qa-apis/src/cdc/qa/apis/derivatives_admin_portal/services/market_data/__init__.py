from dataclasses import dataclass, field

import requests

from .valuation_node import ValuationNodeService


@dataclass(frozen=True)
class MarketDataServices:
    host: str = field()
    session: requests.Session = field(default_factory=requests.Session)

    valuation_node: ValuationNodeService = field(init=False)

    def __post_init__(self):
        services = {
            "valuation_node": ValuationNodeService,
        }

        for k, v in services.items():
            object.__setattr__(self, k, v(host=self.host, session=self.session))
