from dataclasses import InitVar, dataclass, field

import requests

from .services.account import AccountService, GetAccountSummaryApi
from .services.deriv import DerivGetTransferHistoryApi, DerivService, DerivTransferApi
from .services.margin import MarginService
from .services.orders import (
    CancelAllOrdersApi,
    CancelOrderApi,
    CreateOrderApi,
    GetOpenOrdersApi,
    GetOrderDetailApi,
    GetOrderHistoryApi,
    CreateOrderListApi,
    CancelOrderListApi,
    OrderService,
)
from .services.otc import OTCService
from .services.sub_account import SubAccountService
from .services.trades import GetTradesApi, TradesService

__all__ = [
    "PrivateServices",
    "OrderService",
    "CancelAllOrdersApi",
    "CancelOrderApi",
    "CreateOrderApi",
    "GetOpenOrdersApi",
    "GetOrderDetailApi",
    "GetOrderHistoryApi",
    "CreateOrderListApi",
    "CancelOrderListApi",
    "AccountService",
    "GetAccountSummaryApi",
    "TradesService",
    "GetTradesApi",
    "DerivService",
    "DerivTransferApi",
    "DerivGetTransferHistoryApi",
    "MarginService",
    "SubAccountService",
    "OTCService",
]


@dataclass(frozen=True)
class PrivateServices:
    api_key: InitVar[str] = field()
    secret_key: InitVar[str] = field()

    host: str = field()
    session: requests.Session = field(default_factory=requests.Session)

    order: OrderService = field(init=False)
    account: AccountService = field(init=False)
    trades: TradesService = field(init=False)
    deriv: DerivService = field(init=False)
    margin: MarginService = field(init=False)
    sub_account: SubAccountService = field(init=False)
    otc: OTCService = field(init=False)

    def __post_init__(self, api_key, secret_key):
        services = {
            "order": OrderService,
            "account": AccountService,
            "trades": TradesService,
            "deriv": DerivService,
            "margin": MarginService,
            "sub_account": SubAccountService,
            "otc": OTCService,
        }

        for k, v in services.items():
            object.__setattr__(self, k, v(host=self.host, session=self.session, api_key=api_key, secret_key=secret_key))
