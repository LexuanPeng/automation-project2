from dataclasses import InitVar, dataclass, field

import requests

from .services.account import (
    AccountService,
    CreateWithdrawalApi,
    ChangeAccountLeverageApi,
    GetCurrencyNetworksApi,
    GetSubAccountBalancesApi,
    UserBalanceApi,
    GetDepositAddressApi,
    CreateSubaccountTransferApi,
    UserBalanceHistoryApi,
    GetAccountsApi,
)
from .services.orders import (
    OrderService,
    GetOpenOrdersApi,
    CancelOrderApi,
    CreateOrderApi,
    CancelAllOrdersApi,
    GetOrderDetailApi,
    GetOrderHistoryApi,
    CreateOrderListApi,
    CancelOrderListApi,
    GetOrderListApi,
)
from .services.positions import PositionsService, GetPositionsApi, ClosePositionApi
from .services.trades import TradesService, GetTradesApi, GetTransactionsApi, ConvertCollateralApi
from .services.otc import (
    OTCService,
    GetOTCUserApi,
    GetInstrumentsApi,
    RequestQuoteApi,
    AcceptQuoteApi,
    GetQuoteHistoryApi,
    GetTradeHistoryApi,
)

__all__ = [
    "PrivateServices",
    "AccountService",
    "CreateWithdrawalApi",
    "ChangeAccountLeverageApi",
    "GetCurrencyNetworksApi",
    "GetSubAccountBalancesApi",
    "UserBalanceApi",
    "GetDepositAddressApi",
    "CreateSubaccountTransferApi",
    "UserBalanceHistoryApi",
    "GetAccountsApi",
    "OrderService",
    "GetOpenOrdersApi",
    "CancelOrderApi",
    "CreateOrderApi",
    "CancelAllOrdersApi",
    "GetOrderDetailApi",
    "GetOrderHistoryApi",
    "CreateOrderListApi",
    "CancelOrderListApi",
    "GetOrderListApi",
    "PositionsService",
    "GetPositionsApi",
    "ClosePositionApi",
    "TradesService",
    "GetTradesApi",
    "GetTransactionsApi",
    "ConvertCollateralApi",
    "OTCService",
    "GetOTCUserApi",
    "GetInstrumentsApi",
    "RequestQuoteApi",
    "AcceptQuoteApi",
    "GetQuoteHistoryApi",
    "GetTradeHistoryApi",
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
    positions: PositionsService = field(init=False)
    otc: OTCService = field(init=False)

    def __post_init__(self, api_key, secret_key):
        services = {
            "order": OrderService,
            "account": AccountService,
            "trades": TradesService,
            "positions": PositionsService,
            "otc": OTCService,
        }

        for k, v in services.items():
            object.__setattr__(self, k, v(host=self.host, session=self.session, api_key=api_key, secret_key=secret_key))
