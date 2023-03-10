from dataclasses import dataclass, field

import requests
from pydantic import Field

from .services.account import AccountServices
from .services.product import ProductServices
from .services.market_data import MarketDataServices
from .services.global_data import GlobalServices


@dataclass(frozen=True)
class AdminPortalServices:
    host: str = field(default="https://dstg-internal-ui.x.3ona.co/v1/")
    session: requests.Session = field(default_factory=requests.Session)

    account: AccountServices = Field(init=False)
    product: ProductServices = Field(init=False)
    market_data: MarketDataServices = Field(init=False)
    global_data: GlobalServices = Field(init=False)

    def __post_init__(self):
        services = {
            "account": AccountServices,
            "product": ProductServices,
            "market_data": MarketDataServices,
            "global_data": GlobalServices,
        }

        for k, v in services.items():
            object.__setattr__(self, k, v(host=self.host, session=self.session))
