import logging
import re
from urllib.parse import urljoin

import requests

from ..models.login_exception import NoRedirectUrlException

logger = logging.getLogger(__name__)


class SalesPortalAuthService:
    def __init__(
        self,
        user_email: str,
        user_password: str,
        sales_portal_host: str = "https://sit-otctrading-sales-portal-server.x.3ona.co/",
        okta_authn_url: str = "https://dev-00260318.okta.com/api/v1/authn/",
        session=None,
    ):
        """
        user_info stores the user email, password and otp_secret
        :param user_email: user email
        :param user_password: user password
        :param sales_portal_host:
        :param okta_authn_url:
        :param session
        """
        self.user_email = user_email
        self.password = user_password
        self.sales_portal_host = sales_portal_host
        self.okta_authn_url = okta_authn_url

        self.header = {"Accept": "application/json"}
        self.session = requests.Session() if session is None else session

        self.sales_login_okta_url = urljoin(self.sales_portal_host, "fe-sp-api/login/okta")
        self.token = None

    def login(self) -> str:
        """
        step1: https://sit-otctrading-sales-portal-server.x.3ona.co/fe-sp-api/login/okta
        step2: get step1 redirect url
        https://dev-00260318.okta.com/oauth2/default/v1/authorize?response_type=code&client_id=0oa3umgel8W58DfoZ5d7
        &scope=openid%20profile%20email%20address%20phone%20offline_access
        &state=eyJzdGF0ZSI6Im03WDZBcWhSbGNGYjctNU9kOEVXMngzQlNCazduUEhxOEMtTkM0Z1I1cTQ9Iiwic2Vzc2lvbklkIjoiN2VkYjQ3
        Y2ItZWFlMi00OGU1LTlmYjAtMDUwNDdhNzUwYzVjIn0%3D
        &redirect_uri=https://sit-otctrading-sales-portal-server.x.3ona.co/fe-sp-api/login/okta/code
        &nonce=bDGaFQGlQbY0EMTBDCjveqoWa85I2rr7AOVG3ajOt9w
        step3: get step2 redirect url
        https://dev-00260318.okta.com/login/step-up/redirect?stateToken=00EXtv6HQE2-me3g8dhG_R5qt5NxfCu-N5WRCu29NA
        and put the stateToken as one of the parameters in step 4
        step4: authenticates a user with username/password credentials
        step5: access okta step up url
        https://dev-00260318.okta.com/login/step-up/redirect?stateToken=00EXtv6HQE2-me3g8dhG_R5qt5NxfCu-N5WRCu29NA
        step6: redirect to url
        https://sit-otctrading-sales-portal-server.x.3ona.co/fe-sp-api/login/okta/code?
        code=KPAoTMAE70DOIijB0ihqPAy1pqhdu8naXOO1vLqbXvE
        &state=eyJzdGF0ZSI6Im03WDZBcWhSbGNGYjctNU9kOEVXMngzQlNCazduUEhxOEMtTkM0Z1I1cTQ9Iiwic2Vzc2lvb
        klkIjoiN2VkYjQ3Y2ItZWFlMi00OGU1LTlmYjAtMDUwNDdhNzUwYzVjIn0%3D
        and get the token
        :return:
        Returns:
            str: token
        """
        logger.info(f"start sign in email: {self.user_email} ...")
        # access authorize
        # get okta step up url
        okta_step_up_url = self._access_authorize()
        state_token = okta_step_up_url[-42:]

        # okta authenticates the user
        self._okta_authn(state_token)
        # get okta token
        code_url = self._access_okta_step_up_url(okta_step_up_url)

        # get sales portal token
        self._access_sales_portal_token_url(code_url)
        return self.token

    def _access_okta_step_up_url(self, url: str) -> str:
        logger.debug(f"access okta step up url: {url}")
        response = self.session.get(url, allow_redirects=False)
        redirect_url = response.headers.get("location", None)
        logger.debug(f"get response redirect url: {redirect_url}")

        if not redirect_url:
            logger.error("Access okta step up failed with NONE redirect url!")
            raise NoRedirectUrlException("Access okta step up failed with NONE redirect url!")
        return redirect_url

    def _access_sales_portal_token_url(self, url: str):
        logger.debug(f"access token url: {url}")
        response = self.session.get(url, allow_redirects=False)
        token = response.headers.get("token", None)
        if token:
            self.token = token
        else:
            logger.error(f"Get token failed! {url=}")
            raise Exception(f"Get token failed! {url=}")

    def _access_authorize(self) -> str:
        try:
            logger.debug(f"access sales portal login okta url: {self.sales_login_okta_url}")
            resp = self.session.get(self.sales_login_okta_url)
            logger.debug(f"sales portal login okta response: {resp.text}")
            okta_authorize_url = resp.json()["redirect"]

            logger.debug(f"access okta authorize url: {okta_authorize_url}")
            resp = self.session.get(okta_authorize_url, allow_redirects=True)
            okta_step_up_url = re.findall(r"href='(.*?)'", resp.text)[0]
            logger.debug(f"get response okta step up url: {okta_step_up_url}")

            if not okta_step_up_url:
                logger.error("Access authorize failed with NONE stateToken url!")
                raise NoRedirectUrlException("Primary authentication failed with NONE statetoken url!")
            return okta_step_up_url
        except Exception as e:
            raise Exception(f"get okta step up url failed! Error:{str(e)}")

    def _okta_authn(self, state_token: str):
        logger.debug(f"okta authn url: {self.okta_authn_url}")
        request_data = {
            "username": self.user_email,
            "password": self.password,
            "options": {
                "multiOptionalFactorEnroll": True,
                "warnBeforePasswordExpired": True,
            },
            "stateToken": state_token,
        }
        result = self.session.post(self.okta_authn_url, json=request_data, headers=self.header, allow_redirects=False)
        logger.debug(f"okta authn result: {result.json()}")
        if result.status_code != 200:
            logger.error(f"Primary authentication failed, email: {self.user_email}, password: {self.password}")
            raise NoRedirectUrlException("Primary authentication failed with NONE redirect url!")
