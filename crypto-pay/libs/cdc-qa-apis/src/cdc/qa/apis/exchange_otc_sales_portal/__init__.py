import logging
from dataclasses import dataclass, field

import requests

from .services.auth import SalesPortalAuthService
from .services.sales_portal import SalesPortalService

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class OTCSalesPortalService:
    host: str = field(default="https://sit-otctrading-sales-portal-server.x.3ona.co/")
    session: requests.Session = field(default_factory=requests.Session)
    token: str = field(default="")

    # services
    sales_portal: SalesPortalService = field(init=False)

    def login(
        self,
        user_email: str,
        user_password: str,
        sales_portal_host: str = "https://sit-otctrading-sales-portal-server.x.3ona.co/",
        okta_authn_url: str = "https://dev-00260318.okta.com/api/v1/authn/",
    ):
        if not self.token:
            logger.info("sales portal token is null, login...")
            auth_service = SalesPortalAuthService(
                user_email=user_email,
                user_password=user_password,
                sales_portal_host=sales_portal_host,
                okta_authn_url=okta_authn_url,
                session=self.session,
            )
            token = auth_service.login()
            logger.info(f"login success get sales portal token:{token}")
            object.__setattr__(self, "token", token)
            self.__post_init__()

        return self.token

    def __post_init__(self):
        services = {
            "sales_portal": SalesPortalService,
        }
        for k, v in services.items():
            object.__setattr__(self, k, v(host=self.host, session=self.session, token=self.token))
