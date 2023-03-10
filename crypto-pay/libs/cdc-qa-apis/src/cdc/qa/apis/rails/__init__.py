from dataclasses import dataclass, field

import requests

from .models import RailsResponse, RailsResponseError
from .services.account import AccountService
from .services.address import AddressService
from .services.app import AppService
from .services.auth import AuthService
from .services.card import CardService
from .services.fiat import FiatService
from .services.malta_entity import MaltaEntityService
from .services.manual_jumio import ManualJumioService
from .services.mco_lockup import MCOLockupService
from .services.user import UserService
from .services.terms import TermsService
from .services.totp import TotpService
from .services.credit import CreditService
from .services.exchanges import ExchangesService
from .services.crypto_wallets import CryptoWalletsService
from .services.earn import EarnService
from .services.recurring_buy import RecurringBuyService
from .services.supermenu import SupermenuService
from .services.plaid import PlaidService
from .services.paystring import PayStringService
from .services.withdraw import WithdrawService
from .services.balances import BalancesService
from .services.dust_conversion import DustConversionService
from .services.mobile_airtime import MobileAirtimeService
from .services.transfer import TransferService
from .services.target_price import TargetPriceService
from .services.gift_card import GiftCardService
from .services.supercharger import SuperchargerService
from .services.withdraw import WithdrawService
from .services.kyc_info import KYCInfoService


@dataclass(frozen=True)
class RailsApi:
    _host: str = field(default="https://st.mona.co/api/")
    _session: requests.Session = field(default_factory=requests.Session)
    _env: str = field(default="stg")

    account: AccountService = field(init=False)
    address: AddressService = field(init=False)
    app: AppService = field(init=False)
    auth: AuthService = field(init=False)
    card: CardService = field(init=False)
    fiat: FiatService = field(init=False)
    manual_jumio: ManualJumioService = field(init=False)
    mco_lockup: MCOLockupService = field(init=False)
    user: UserService = field(init=False)
    terms: TermsService = field(init=False)
    totp: TotpService = field(init=False)
    credit: CreditService = field(init=False)
    exchanges: ExchangesService = field(init=False)
    crypto_wallets: CryptoWalletsService = field(init=False)
    earn: EarnService = field(init=False)
    recurring_buy: RecurringBuyService = field(init=False)
    supermenu: SupermenuService = field(init=False)
    plaid: PlaidService = field(init=False)
    malta_entity: MaltaEntityService = field(init=False)
    balances: BalancesService = field(init=False)
    dust_conversion: DustConversionService = field(init=False)
    mobile_airtime: MobileAirtimeService = field(init=False)
    transfer: TransferService = field(init=False)
    target_price: TargetPriceService = field(init=False)
    gift_card: GiftCardService = field(init=False)
    supercharger: SuperchargerService = field(init=False)
    withdraw: WithdrawService = field(init=False)
    kyc_info: KYCInfoService = field(init=False)

    def __post_init__(self):
        def raise_for_error(_r):
            content = _r.content
            response = RailsResponse.parse_raw(b=content)
            if not response.ok:
                raise RailsResponseError(f"{response.error=} content={content.decode('utf-8')}")

        self._session.hooks["response"].append(lambda r, *args, **kwargs: r.raise_for_status())
        self._session.hooks["response"].append(lambda r, *args, **kwargs: raise_for_error(r))

        services = {
            "account": AccountService,
            "address": AddressService,
            "app": AppService,
            "auth": AuthService,
            "card": CardService,
            "fiat": FiatService,
            "manual_jumio": ManualJumioService,
            "mco_lockup": MCOLockupService,
            "user": UserService,
            "terms": TermsService,
            "totp": TotpService,
            "credit": CreditService,
            "exchanges": ExchangesService,
            "crypto_wallets": CryptoWalletsService,
            "earn": EarnService,
            "recurring_buy": RecurringBuyService,
            "supermenu": SupermenuService,
            "plaid": PlaidService,
            "paystring": PayStringService,
            "withdraw": WithdrawService,
            "malta_entity": MaltaEntityService,
            "balances": BalancesService,
            "dust_conversion": DustConversionService,
            "mobile_airtime": MobileAirtimeService,
            "transfer": TransferService,
            "target_price": TargetPriceService,
            "gift_card": GiftCardService,
            "supercharger": SuperchargerService,
            "kyc_info": KYCInfoService,
        }

        for k, v in services.items():
            secret_id = "railsapi_dev" if self._env == "dev" else "railsapi"
            object.__setattr__(self, k, v(host=self._host, session=self._session, env=self._env, secret_id=secret_id))
