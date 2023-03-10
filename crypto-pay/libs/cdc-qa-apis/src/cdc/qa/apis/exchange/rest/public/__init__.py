from dataclasses import dataclass, field, InitVar

import requests

from .services.instruments import InstrumentsService, GetInstrumentsApi
from .services.order_book import BookService, GetBookApi
from .services.candlestick import CandlestickService, GetCandlestickApi
from .services.ticker import TickerService, GetTickerApi
from .services.trades import TradesService, GetTradesApi
from .services.margin import MarginService, GetTransferCurrenciesApi, GetLoanCurrenciesApi


__all__ = [
    "PublicServices",
    "InstrumentsService",
    "GetInstrumentsApi",
    "BookService",
    "GetBookApi",
    "CandlestickService",
    "GetCandlestickApi",
    "TickerService",
    "GetTickerApi",
    "TradesService",
    "GetTradesApi",
    "MarginService",
    "GetLoanCurrenciesApi",
    "GetTransferCurrenciesApi",
]


@dataclass(frozen=True)
class PublicServices:
    api_key: InitVar[str] = field()
    secret_key: InitVar[str] = field()

    host: str = field()
    session: requests.Session = field(default_factory=requests.Session)

    instruments: InstrumentsService = field(init=False)
    book: BookService = field(init=False)
    candlestick: CandlestickService = field(init=False)
    ticker: TickerService = field(init=False)
    trades: TradesService = field(init=False)
    margin: MarginService = field(init=False)

    def __post_init__(self, api_key, secret_key):
        services = {
            "instruments": InstrumentsService,
            "book": BookService,
            "candlestick": CandlestickService,
            "ticker": TickerService,
            "trades": TradesService,
            "margin": MarginService,
        }

        for k, v in services.items():
            object.__setattr__(self, k, v(host=self.host, session=self.session, api_key=api_key, secret_key=secret_key))
