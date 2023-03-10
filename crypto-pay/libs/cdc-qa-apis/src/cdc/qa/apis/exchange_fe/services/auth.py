import logging
import re
import time
from urllib.parse import urlencode, urljoin

import pyotp
import requests

from ..models.login_exception import NoCsrfTokenException, NoRedirectUrlException

logger = logging.getLogger(__name__)


class ExchangeAuthService:
    def __init__(
        self,
        user_email: str,
        user_password: str,
        otp_secret: str = None,
        mona_host: str = "https://st.mona.co/",
        client_id: str = "8e894f91491c11fed5f693d35dec449ff1e6141c89227c0a860925e365a9854c",
        login_api_host: str = "https://xdev-www.3ona.co/fe-ex-api/",
        session=None,
    ):
        """
        user_info stores the user email, password and otp_secret
        :param user_email: user email
        :param user_password: user password
        :param otp_secret: OTP Secert, used it to generate otp code
        :param mona_host:
        :param client_id:
        :param login_api_host:
        :param session
        """
        self.user_email = user_email
        self.password = user_password
        self.otp_secret = otp_secret
        self.mona_host = mona_host
        self.client_id = client_id

        self.header = {"Content-Type": "application/x-www-form-urlencoded"}
        self.session = requests.Session() if session is None else session

        self.redirect_uri = urljoin(login_api_host, "oauth_redirect")
        self.sign_in_url = urljoin(self.mona_host, "users/sign_in")
        self.otp_check_url = urljoin(self.mona_host, "users/totp/verify")
        self.exchange_token = None
        self.is_otp_verify = False

    def login(self, oauth_authorize_params: dict = None) -> str:
        """
        step1: https://st.mona.co/oauth/authorize?client_id=8e894f91491c11fed5f693d35dec449ff1e6141c89227c0a860925e
              365a9854c&login_type=login&redirect_uri=https%3A%2F%2Fxdev-www.3ona.co%2Ffe-ex-api%2Foauth_redirect&
              response_type=code&scope=
        step2: get step1 redirect url https://st.mona.co/users/sign_in and get the csrf token in response
        step3: post sign in result with email and password and get the redirect url https://st.mona.co/users/totp/verify
        step4: get step3 redirect url https://st.mona.co/users/totp/verify and get the csrf token in response
        step5: TOTP verify and get redirect url https://st.mona.co/oauth/authorize?client_id=8e894f91491c11fed
            5f693d35dec449ff1e6141c89227c0a860925e365a9854c&redirect_uri=https%3A%2F%2Fxdev-www.3ona.co%2Ffe-ex-api%2F
            oauth_redirect&response_type=code&scope=
        step6: redirect to url https://xdev-www.3ona.co/fe-ex-api/oauth_redirect?code=8e68cda40a1013889f8a9670a41ee1154
              b2801861dc8a66b82ded044db4e4b65
        step7: redirect to url https://xdev-www.3ona.co/exchange and get the exchange_token
        :return:

        Args:
            oauth_authorize_params (dict, optional): used for update oauth/authorize? params. Defaults to None.

        Returns:
            str: exchange token
        """
        logger.info(f"start sign in email: {self.user_email} ...")
        # access oauth/authorize
        oauth_url = self._get_oauth_authorize_url(oauth_authorize_params=oauth_authorize_params)
        self._access_oauth(oauth_url)

        # sign
        self._sign_in()

        # otp verify
        if self.is_otp_verify:
            try:
                self._otp_verify()
            except NoRedirectUrlException:
                logger.warning("OTP verify failed, retry it!")
                time.sleep(30 - int(time.time() % 30))
                self._otp_verify()

        # access oauth/authorize none login
        oauth_url_back = self._get_oauth_authorize_url(for_login=False, oauth_authorize_params=oauth_authorize_params)
        token_url = self._access_oauth(oauth_url_back, for_login=False)

        # get token
        self._access_token_url(token_url)
        return self.exchange_token

    def _access_token_url(self, url):
        logger.debug(f"access token url: {url}")
        response = self.session.get(url, allow_redirects=False)
        token = response.cookies.get("token")
        if token:
            self.exchange_token = token
        else:
            logger.error(f"Get token failed! {url=}")
            raise Exception(f"Get token failed! {url=}")

    def _access_oauth(self, url, for_login: bool = True):
        resp = self.session.get(url, allow_redirects=False)
        logger.debug(f"access url: {url}")
        redirect_url = resp.headers.get("Location", None)
        logger.debug(f"get response location: {redirect_url}")

        if not redirect_url:
            logger.error("Access oauth failed with NONE redirect url! " + "before" if for_login else "after" + " login")
            raise NoRedirectUrlException("Otp verify failed with NONE redirect url!")
        if for_login:
            if "users/sign_in" not in redirect_url:
                logger.error(f"Access oauth page failed! access:{url}, redirect url: {redirect_url}")
                raise Exception(f"Access oauth page failed! access:{url}, redirect url: {redirect_url}")
        else:
            if "oauth_redirect?code=" not in redirect_url:
                logger.error(f"Access oauth back page failed! access:{url}, redirect url: {redirect_url}")
                raise Exception(f"Access oauth back page failed! access:{url}, redirect url: {redirect_url}")
        return redirect_url

    def _get_oauth_authorize_url(self, for_login: bool = True, oauth_authorize_params: dict = None):
        oauth_authorize = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": "exapi",
        }
        if oauth_authorize_params:
            oauth_authorize.update(oauth_authorize_params)

        if for_login:
            oauth_authorize["login_type"] = "login"

        url_encode = urlencode(oauth_authorize)
        authorize_oauth_url = urljoin(self.mona_host, f"oauth/authorize?{url_encode}")
        return authorize_oauth_url

    def get_exchange_token(self):
        if self.exchange_token is not None:
            return self.exchange_token
        else:
            return None

    def _sign_in(self):
        logger.debug(f"sign in url: {self.sign_in_url}")
        sign_csrf_token = self._get_csrf_token(self.sign_in_url)
        request_data = {
            "utf8": "✓",
            "authenticity_token": sign_csrf_token,
            "user[email]": self.user_email,
            "user[password]": self.password,
            "button": "",
        }
        result = self.session.post(self.sign_in_url, data=request_data, headers=self.header, allow_redirects=False)
        redirect_url = result.headers.get("location", None)
        logger.debug(f"sign redirect url: {redirect_url}")
        if not redirect_url:
            logger.error(f"Sign in failed, email: {self.user_email}, password: {self.password}")
            raise NoRedirectUrlException("Sign in failed with NONE redirect url!")

        if "totp/verify" in redirect_url:
            self.is_otp_verify = True
        elif "oauth/authorize" in redirect_url:
            self.is_otp_verify = False
        elif "users/sign_in" in redirect_url:
            logger.error(f"Sign in failed! redirect:{redirect_url}")
            raise Exception(f"Sign in failed! redirect:{redirect_url}")
        else:
            logger.error(f"Sign in failed! unknown redirect:{redirect_url}")
            raise Exception(f"Sign in failed! unknown redirect:{redirect_url}")

    def _otp_verify(self):
        logger.debug(f"otp verify url: {self.otp_check_url}")
        otp_csrf_token = self._get_csrf_token(self.otp_check_url)

        totp = pyotp.TOTP(self.otp_secret)
        # make sure time left more than 3 secondes
        left_seconds = 3
        if int(time.time() * 1000 % 30000) >= (30 - left_seconds) * 1000:
            time.sleep(left_seconds)
        code = totp.now()

        request_data = {
            "utf8": "✓",
            "authenticity_token": otp_csrf_token,
            "form[otp][digit1]": code[0],
            "form[otp][digit2]": code[1],
            "form[otp][digit3]": code[2],
            "form[otp][digit4]": code[3],
            "form[otp][digit5]": code[4],
            "form[otp][digit6]": code[5],
        }
        result = self.session.post(self.otp_check_url, data=request_data, headers=self.header, allow_redirects=False)
        redirect_url = result.headers.get("location", None)
        logger.debug(f"otp verify redirect url: {redirect_url}")
        if not redirect_url:
            logger.error("Otp verify failed with NONE redirect url!")
            raise NoRedirectUrlException("Otp verify failed with NONE redirect url!")
        if "totp/verify" in redirect_url or "users/sign_in" in redirect_url:
            logger.error(f"Otp verify failed! redirect:{redirect_url}")
            raise Exception(f"Otp verify failed! redirect:{redirect_url}")

        if "oauth/authorize" not in redirect_url:
            logger.error(f"Otp verify redirects to unknown page:{redirect_url}")
            raise Exception(f"Otp verify redirects to unknown page:{redirect_url}")
        return redirect_url

    def _get_csrf_token(self, url):
        response = self.session.get(url)
        searchObj = re.search(r'<meta name="csrf-token" content="(.*?)" />', response.text)
        if searchObj:
            csrf_token = searchObj.group(1)
        else:
            logger.error(f"Failed to find the csrf token in response, url is {url}")
            raise NoCsrfTokenException(f"Failed to find the csrf token! url is {url}")
        return csrf_token
