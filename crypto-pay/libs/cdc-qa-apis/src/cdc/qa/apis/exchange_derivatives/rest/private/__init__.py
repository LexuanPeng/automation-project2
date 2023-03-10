from dataclasses import dataclass, field, InitVar

import requests

from .services.orders import (
    OrderService,
    CancelAllOrdersApi,
    CancelOrderApi,
    CreateOrderApi,
    GetOpenOrdersApi,
    GetOrderDetailApi,
    GetOrderHistoryApi,
)
from .services.account import AccountService, UserBalanceApi
from .services.positions import PositionsService, GetPositionsApi, ClosePositionApi
from .services.trades import TradesService, GetTradesApi, GetTransactionsApi, ConvertCollateralApi

__all__ = [
    "PrivateServices",
    "OrderService",
    "CancelAllOrdersApi",
    "CancelOrderApi",
    "CreateOrderApi",
    "GetOpenOrdersApi",
    "GetOrderDetailApi",
    "GetOrderHistoryApi",
    "AccountService",
    "UserBalanceApi",
    "GetAccountSummaryApi",
    "PositionsService",
    "ClosePositionApi",
    "GetPositionsApi",
    "TradesService",
    "GetTradesApi",
    "GetTransactionsApi",
    "ConvertCollateralApi",
]


@dataclass(frozen=True)
class PrivateServices:
    api_key: InitVar[str] = field()
    secret_key: InitVar[str] = field()

    host: str = field()
    session: requests.Session = field(default_factory=requests.Session)

    order: OrderService = field(init=False)
    account: AccountService = field(init=False)
    position: PositionsService = field(init=False)
    trades: TradesService = field(init=False)

    def __post_init__(self, api_key, secret_key):
        services = {
            "order": OrderService,
            "account": AccountService,
            "position": PositionsService,
            "trades": TradesService,
        }

        for k, v in services.items():
            object.__setattr__(self, k, v(host=self.host, session=self.session, api_key=api_key, secret_key=secret_key))
