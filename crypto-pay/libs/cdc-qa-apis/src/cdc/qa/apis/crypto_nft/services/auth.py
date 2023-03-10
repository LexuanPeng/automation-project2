import requests
import time
import logging
import pyotp
import string
import random

from .login import LoginService
from .profile import ProfileService

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, host, email: str, password: str, session=None):
        self.host = host
        self.email = email
        self.password = password
        self.headers = {"content-type": "application/json"}
        self.session = requests.Session() if session is None else session
        self.login_service = LoginService(host=self.host)
        self.profile_service = ProfileService(host=self.host)
        self.nft_token = None

    def _generate_token(self, token: str):
        if "Bearer " not in token:
            token = f"Bearer {token}"
        self.nft_token = token

    @staticmethod
    def get_totp_verify_code(totp_seed):
        totp = pyotp.TOTP(totp_seed)
        left_seconds = 3
        if int(time.time() * 1000 % 30000) >= (30 - left_seconds) * 1000:
            time.sleep(left_seconds)
        totp_code = totp.now()
        return totp_code

    def _get_otp_code(self, otp_type: int = 1, seed: str = None) -> dict:
        """
        otp_type: 1-otpCode, 2-emailOtpCode, 3-clientOtpCode, 4-smsOtpCode
        """
        otp_code: dict = {
            1: {"otpCode": "12345678"},
            2: {"emailOtpCode": "12345678"},
            3: {"clientOtpCode": "12345678"},
            4: {"smsOtpCode": "12345678"},
        }
        if otp_type == 3:
            return {"clientOtpCode": self.get_totp_verify_code(seed)}
        else:
            if "k6-nft-load-test" in self.email:
                return otp_code.get(otp_type, {})

    def email_login(self):
        """
        step 1: authenticate
        step 2: prepare otp
        step 3: authenticate with otp
        Returns: auth.AuthenticateWithOtpResponse
        """
        step1_resp = self.login_service.authenticate(email=self.email, password=self.password)
        try:
            self._generate_token(step1_resp.data.authenticate.token)
            step2_resp = self.login_service.prepare_otp(self.nft_token)
            if step2_resp.data.prepareOtp.success:
                step3_resp = self.login_service.auth_with_otp(otp_code=self._get_otp_code(1), token=self.nft_token)
                self._generate_token(step3_resp.data.authenticateWithOtp.token)
                return self.nft_token, step3_resp
            assert "Login failed"
        except KeyError:
            assert "Login failed"

    def email_unify_login(self, seed: str = None, email_title: str = None, re_content: str = None, gmail_obj=None):
        """
        step 1: authenticate by email
        step 2: prepare otp
        step 3: continue auth
        Returns: auth.ContinueAuthResponse
        """
        is_complet_profile = False
        step1_resp = self.login_service.auth_by_email(email=self.email, password=self.password)

        if "CompleteProfile" in step1_resp.data.authenticateByEmail.requiredSteps:
            is_complet_profile = True

        self._generate_token(step1_resp.data.authenticateByEmail.token)
        if "ClientOtp" in step1_resp.data.authenticateByEmail.requiredSteps:
            otp_code = self._get_otp_code(otp_type=3, seed=seed)
        elif "EmailOtp" in step1_resp.data.authenticateByEmail.requiredSteps:
            step2_resp = self.login_service.prepare_otp(self.nft_token)
            assert step2_resp.data.prepareOtp.success is True
            if "k6-nft-load-test" in self.email:
                otp_code = self._get_otp_code(2)
            else:
                email_code = gmail_obj.get_email_target_text(email_title=email_title, re_content=re_content)
                otp_code = {"emailOtpCode": email_code}
        else:
            otp_code = self._get_otp_code(2)

        step3_resp = self.login_service.continue_auth(otp_code=otp_code, token=self.nft_token)
        if step3_resp.data is None:
            logger.error("the 3rd step sign in fialed.")
            logger.warning("wait 60 seconds to sign in again...")
            time.sleep(60)

            if "ClientOtp" in step1_resp.data.authenticateByEmail.requiredSteps:
                otp_code = self._get_otp_code(otp_type=3, seed=seed)
            elif "EmailOtp" in step1_resp.data.authenticateByEmail.requiredSteps:
                step2_resp = self.login_service.prepare_otp(self.nft_token)
                assert step2_resp.data.prepareOtp.success is True
                if "k6-nft-load-test" in self.email:
                    otp_code = self._get_otp_code(2)
                else:
                    email_code = gmail_obj.get_email_target_text(email_title=email_title, re_content=re_content)
                    otp_code = {"emailOtpCode": email_code}
            else:
                otp_code = self._get_otp_code(2)

            step3_resp = self.login_service.continue_auth(otp_code=otp_code, token=self.nft_token)

        self._generate_token(step3_resp.data.continueAuthentication.token)

        if is_complet_profile:
            username = "".join(random.choices(string.ascii_lowercase, k=8))
            self.profile_service.complete_profile(name=username, username=username, token=self.nft_token)
        return self.nft_token, step3_resp

    def qrcode_login(self):
        pass

    def get_nft_token(self):
        if self.nft_token is not None:
            return self.nft_token
        else:
            return None
