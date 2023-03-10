import logging
import requests
from dataclasses import dataclass, field

from .services.auth import AuthService
from .services.common import CommonService
from .services.collections import CollectionsService
from .services.login import LoginService
from .services.drops import DropsService
from .services.marketplace import MarketplaceService
from .services.profile import ProfileService
from .services.assets import AssetsService
from .services.offers import OffersService
from .services.create_nft import CreateNftService
from .services.marketplace import MarketplaceService
from .services.user_behavior import UserBehaviorService

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class GqlServices:
    host: str = field(default="https://3ona.co/nft-api/graphql")
    session: requests.Session = field(default_factory=requests.Session)
    nft_token: str = field(default="")

    login: LoginService = field(init=False)
    drops: DropsService = field(init=False)
    collections: CollectionsService = field(init=False)
    common: CommonService = field(init=False)
    profile: ProfileService = field(init=False)
    assets: AssetsService = field(init=False)
    offers: OffersService = field(init=False)
    create_nft: CreateNftService = field(init=False)
    marketplace: MarketplaceService = field(init=False)
    user_behavior: UserBehaviorService = field(init=False)

    def authentication(
        self,
        email: str,
        password: str,
        login_type: str = "unify",
        seed: str = None,
        email_title: str = None,
        re_content: str = None,
        gmail_obj=None,
    ):
        resp = {}
        if not self.nft_token:
            logger.info("NFT token is null, login...")
            auth_service = AuthService(host=self.host, email=email, password=password, session=self.session)
            if login_type == "unify":
                token, resp = auth_service.email_unify_login(
                    seed=seed, email_title=email_title, re_content=re_content, gmail_obj=gmail_obj
                )
            elif login_type == "old":
                token, resp = auth_service.email_login()
            else:
                token = self.nft_token
            logger.info(f"login success get nft token: {token}")
            object.__setattr__(self, "nft_token", token)
            self.__post_init__()
        return self.nft_token, resp

    def __post_init__(self):
        services = {
            "login": LoginService,
            "drops": DropsService,
            "profile": ProfileService,
            "offers": OffersService,
            "assets": AssetsService,
            "collections": CollectionsService,
            "common": CommonService,
            "create_nft": CreateNftService,
            "marketplace": MarketplaceService,
            "user_behavior": UserBehaviorService,
        }

        for k, v in services.items():
            object.__setattr__(self, k, v(host=self.host, session=self.session, nft_token=self.nft_token))
