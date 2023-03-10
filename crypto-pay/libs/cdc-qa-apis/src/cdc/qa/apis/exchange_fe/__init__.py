import logging
from dataclasses import dataclass, field

import requests

from .services.account import AccountService
from .services.addr import AddressService
from .services.auth import ExchangeAuthService
from .services.common import CommonService
from .services.finance import FinanceService
from .services.security import SecurityService
from .services.user import UserService
from .services.sub_account import SubAccountService

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class FeExchangeService:
    host: str = field(default="https://xdev4-www.3ona.co/fe-ex-api/")
    session: requests.Session = field(default_factory=requests.Session)
    exchange_token: str = field(default="")

    # services
    user: UserService = field(init=False)
    finance: FinanceService = field(init=False)
    account: AccountService = field(init=False)
    common: CommonService = field(init=False)
    addr: AddressService = field(init=False)
    sub_account: SubAccountService = field(init=False)
    security: SecurityService = field(init=False)

    def login(
        self,
        user_email: str,
        user_password: str,
        otp_secret: str,
        mona_host: str = "https://st.mona.co/",
        client_id: str = "8e894f91491c11fed5f693d35dec449ff1e6141c89227c0a860925e365a9854c",
        login_api_host: str = "https://xdev-www.3ona.co/fe-ex-api/",
        oauth_authorize_params: dict = None,
    ):
        if not self.exchange_token:
            logger.info("exchange token is null, login...")
            auth_service = ExchangeAuthService(
                user_email=user_email,
                user_password=user_password,
                otp_secret=otp_secret,
                mona_host=mona_host,
                client_id=client_id,
                login_api_host=login_api_host,
                session=self.session,
            )
            token = auth_service.login(oauth_authorize_params=oauth_authorize_params)
            logger.info(f"login success get exchange token:{token}")
            object.__setattr__(self, "exchange_token", token)
            self.__post_init__()

        return self.exchange_token

    def __post_init__(self):
        services = {
            "user": UserService,
            "finance": FinanceService,
            "account": AccountService,
            "common": CommonService,
            "addr": AddressService,
            "sub_account": SubAccountService,
            "security": SecurityService,
        }
        for k, v in services.items():
            object.__setattr__(self, k, v(host=self.host, session=self.session, exchange_token=self.exchange_token))
