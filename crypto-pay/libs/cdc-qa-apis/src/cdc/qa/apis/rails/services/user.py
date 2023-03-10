import os
from typing import Optional, Union
from cdc.qa.core import secretsmanager as sm
from cdc.qa.apis.common.models.rest_api import HttpMethods

from ..models import RailsRestApi, RailsRestService, BearerAuth, encrypt_passcode
from ..models.user import (
    UserAuthRequestData,
    UserAuthResponse,
    UserPhoneUpdateRequestData,
    UserPhoneUpdateResponse,
    UserPhoneVerifyRequestData,
    UserPhoneVerifyResponse,
    UserTermsUpdateRequestData,
    UserTermsUpdateResponse,
    UserNewslettersUpdateRequestData,
    UserNewslettersUpdateResponse,
    UserNameUpdateRequestData,
    UserNameUpdateResponse,
    UserPasscodeUpdateRequestData,
    UserPasscodeUpdateResponse,
    UserPaymentCurrencyUpdateRequestData,
    UserPaymentCurrencyUpdateResponse,
    UserConfigsSupermenuShortcutsEnabledUpdateRequestData,
    UserConfigsSupermenuShortcutsEnabledUpdateResponse,
    UserConfigsPreferLocaleRequestData,
    UserConfigsPreferLocaleResponse,
    UserConfigResponse,
    UserPhoneSendOtpRequestData,
    UserPhoneSendOtpResponse,
    UserPhoneVerifyOtpRequestData,
    UserPhoneVerifyOtpResponse,
    UserPasscodeVerifyRequestData,
    UserPasscodeVerifyResponse,
    UserShowResponse,
    UserCreatePhoneResponse,
    UserCreateEmailResponse,
    UserUpdateEmailResponse,
    UserUpdateEmailRequestData,
    UserInputReferralCodeRequestData,
    UserInputReferralCodeResponse,
    UserClaimReferralCodeReqeustData,
    UserClaimReferralCodeResponse,
    PasscodeResetInAppInitResponse,
    PasscodeResetInAppCreateRequestData,
    PasscodeResetInAppCreateResponse,
    PasscodeResetInAppResetRequestData,
    PasscodeResetInAppResetResponse,
)


class UserAuthApi(RailsRestApi):
    """Authenticate user before login."""

    path = "user/auth"
    method = HttpMethods.POST
    request_data_type = UserAuthRequestData
    response_type = UserAuthResponse


class UserPhoneUpdateApi(RailsRestApi):
    """Update user phone number."""

    path = "user/phone/update"
    method = HttpMethods.POST
    request_data_type = UserPhoneUpdateRequestData
    response_type = UserPhoneUpdateResponse


class UserPhoneSendOtpApi(RailsRestApi):
    """Update user send otp"""

    path = "user/phone/send_otp"
    method = HttpMethods.POST
    request_data_type = UserPhoneSendOtpRequestData
    response_type = UserPhoneSendOtpResponse


class UserPhoneVerifyOtpApi(RailsRestApi):
    """Update user verify otp"""

    path = "user/phone/verify_otp"
    method = HttpMethods.POST
    request_data_type = UserPhoneVerifyOtpRequestData
    response_type = UserPhoneVerifyOtpResponse


class UserPhoneVerifyApi(RailsRestApi):
    """Verify user phone number."""

    path = "user/phone/verify"
    method = HttpMethods.POST
    request_data_type = UserPhoneVerifyRequestData
    response_type = UserPhoneVerifyResponse


class UserTermsUpdateApi(RailsRestApi):
    """Update user terms option.."""

    path = "user/terms/update"
    method = HttpMethods.POST
    request_data_type = UserTermsUpdateRequestData
    response_type = UserTermsUpdateResponse


class UserNewslettersUpdateApi(RailsRestApi):
    """Update user newsletters option."""

    path = "user/newsletters/update"
    method = HttpMethods.POST
    request_data_type = UserNewslettersUpdateRequestData
    response_type = UserNewslettersUpdateResponse


class UserNameUpdateApi(RailsRestApi):
    """Update user name."""

    path = "user/name/update"
    method = HttpMethods.POST
    request_data_type = UserNameUpdateRequestData
    response_type = UserNameUpdateResponse


class UserPasscodeUpdateApi(RailsRestApi):
    """Update user passcode."""

    path = "user/passcode/update"
    method = HttpMethods.POST
    request_data_type = UserPasscodeUpdateRequestData
    response_type = UserPasscodeUpdateResponse


class UserPasscodeVerifyApi(RailsRestApi):
    """Verify user passcode."""

    path = "user/passcode/verify"
    method = HttpMethods.POST
    request_data_type = UserPasscodeVerifyRequestData
    response_type = UserPasscodeVerifyResponse


class UserPaymentCurrencyUpdateApi(RailsRestApi):
    """Update user payment currency."""

    path = "user/payment_currency/update"
    method = HttpMethods.POST
    request_data_type = UserPaymentCurrencyUpdateRequestData
    response_type = UserPaymentCurrencyUpdateResponse


class UserConfigsSupermenuShortcutsEnabledUpdateApi(RailsRestApi):
    """Update user supermenu shortcuts enabled configs."""

    path = "user/configs/super_menu_shortcuts_enabled/update"
    method = HttpMethods.POST
    request_data_type = UserConfigsSupermenuShortcutsEnabledUpdateRequestData
    response_type = UserConfigsSupermenuShortcutsEnabledUpdateResponse


class UserConfigsApi(RailsRestApi):
    """Get user configs"""

    path = "user/configs"
    method = HttpMethods.GET
    response_type = UserConfigResponse


class UserConfigsPreferLocaleUpdateApi(RailsRestApi):
    """Update prefer locale"""

    path = "user/configs/preferred_locale/update"
    method = HttpMethods.POST
    request_data_type = UserConfigsPreferLocaleRequestData
    response_type = UserConfigsPreferLocaleResponse


class UserShowApi(RailsRestApi):
    """Update show"""

    path = "user/show"
    method = HttpMethods.GET
    response_type = UserShowResponse


class UserCreatePhoneNumberApi(RailsRestApi):
    """User create new phone number"""

    path = "user/phone/create"
    method = HttpMethods.POST
    response_type = UserCreatePhoneResponse


class UserCreateEmailApi(RailsRestApi):
    """User create new email"""

    path = "user/email/create"
    method = HttpMethods.POST
    response_type = UserCreateEmailResponse


class UserUpdateEmailApi(RailsRestApi):
    """User update new email"""

    path = "user/email/update"
    method = HttpMethods.POST
    request_data_type = UserUpdateEmailRequestData
    response_type = UserUpdateEmailResponse


class UserInputReferralCodeApi(RailsRestApi):
    """User input referral code"""

    path = "referrals/verify"
    method = HttpMethods.POST
    request_data_type = UserInputReferralCodeRequestData
    response_type = UserInputReferralCodeResponse


class UserClaimReferralCodeApi(RailsRestApi):
    """User claim referral code"""

    path = "referrals/claim"
    method = HttpMethods.POST
    request_data_type = UserClaimReferralCodeReqeustData
    response_type = UserClaimReferralCodeResponse


class PasscodeResetInAppInitApi(RailsRestApi):
    """PasscodeResetInApp init Api"""

    path = "user/passcode/reset_in_app"
    method = HttpMethods.GET
    response_type = PasscodeResetInAppInitResponse


class PasscodeRestInAppCreateApi(RailsRestApi):
    """PasscodeResetInApp create Api"""

    path = "user/passcode/reset_requests/create"
    method = HttpMethods.POST
    request_data_type = PasscodeResetInAppCreateRequestData
    response_type = PasscodeResetInAppCreateResponse


class PasscodeRestInAppResetApi(RailsRestApi):
    """PasscodeResetInApp reset Api"""

    path = "user/passcode/reset"
    method = HttpMethods.POST
    request_data_type = PasscodeResetInAppResetRequestData
    response_type = PasscodeResetInAppResetResponse


class UserService(RailsRestService):
    def auth(self, email: str) -> UserAuthResponse:
        api = UserAuthApi(host=self.host, _session=self.session)
        AUTH_ACCESS_TOKEN = os.environ.get("AUTH_ACCESS_TOKEN", None)
        AUTH_ACCESS_TOKEN = AUTH_ACCESS_TOKEN or sm.get_secret_json(self.secret_id)["AUTH_ACCESS_TOKEN"]
        auth = BearerAuth(AUTH_ACCESS_TOKEN)
        data = UserAuthRequestData(email=email).dict(exclude_none=True)

        response = api.call(auth=auth, data=data)
        return UserAuthResponse.parse_raw(b=response.content)

    def phone_update(self, phone_number: str, token: str = None) -> UserPhoneUpdateResponse:
        api = UserPhoneUpdateApi(host=self.host, _session=self.session)
        data = UserPhoneUpdateRequestData(phone=phone_number, token=token).dict(exclude_none=True)

        response = api.call(data=data)
        return UserPhoneUpdateResponse.parse_raw(b=response.content)

    def phone_verify(self, otp: Union[str, int]) -> UserPhoneVerifyResponse:
        api = UserPhoneVerifyApi(host=self.host, _session=self.session)
        data = UserPhoneVerifyRequestData(otp=otp).dict(exclude_none=True)

        response = api.call(data=data)
        return UserPhoneVerifyResponse.parse_raw(b=response.content)

    def terms_update(self, terms_of_service: bool) -> UserTermsUpdateResponse:
        api = UserTermsUpdateApi(host=self.host, _session=self.session)
        data = UserTermsUpdateRequestData(terms_of_service=terms_of_service).dict(exclude_none=True)

        response = api.call(data=data)
        return UserTermsUpdateResponse.parse_raw(b=response.content)

    def newsletter_update(self, subscribe_newsletters: bool) -> UserNewslettersUpdateResponse:
        api = UserNewslettersUpdateApi(host=self.host, _session=self.session)
        data = UserNewslettersUpdateRequestData(subscribe_newsletters=subscribe_newsletters).dict(exclude_none=True)

        response = api.call(data=data)
        return UserNewslettersUpdateResponse.parse_raw(b=response.content)

    def name_update(self, name: str) -> UserNameUpdateResponse:
        api = UserNameUpdateApi(host=self.host, _session=self.session)
        data = UserNameUpdateRequestData(name=name).dict(exclude_none=True)

        response = api.call(data=data)
        return UserNameUpdateResponse.parse_raw(b=response.content)

    def passcode_update(self, passcode: str, current_passcode: Optional[str] = None) -> UserPasscodeUpdateResponse:
        api = UserPasscodeUpdateApi(host=self.host, _session=self.session)
        if current_passcode is not None:
            current_passcode = encrypt_passcode(current_passcode)
        data = UserPasscodeUpdateRequestData(passcode=passcode, current_passcode=current_passcode).dict(
            exclude_none=True
        )

        response = api.call(data=data)
        return UserPasscodeUpdateResponse.parse_raw(b=response.content)

    def payment_currency_update(self, payment_currency: str) -> UserPaymentCurrencyUpdateResponse:
        api = UserPaymentCurrencyUpdateApi(host=self.host, _session=self.session)
        data = UserPaymentCurrencyUpdateRequestData(payment_currency=payment_currency).dict(exclude_none=True)

        response = api.call(data=data)
        return UserPaymentCurrencyUpdateResponse.parse_raw(b=response.content)

    def supermenu_shortcuts_enabled_update(
        self, shortcuts_enabled: bool
    ) -> UserConfigsSupermenuShortcutsEnabledUpdateResponse:
        api = UserConfigsSupermenuShortcutsEnabledUpdateApi(host=self.host, _session=self.session)
        data = UserConfigsSupermenuShortcutsEnabledUpdateRequestData(
            super_menu_shortcuts_enabled=shortcuts_enabled
        ).dict(exclude_none=True)

        response = api.call(json=data)
        return UserConfigsSupermenuShortcutsEnabledUpdateResponse.parse_raw(b=response.content)

    def configs(self) -> UserConfigResponse:
        api = UserConfigsApi(host=self.host, _session=self.session)

        response = api.call()
        return UserConfigResponse.parse_raw(b=response.content)

    def update_prefer_locale(self, preferred_locale: str = "en") -> UserConfigsPreferLocaleResponse:
        api = UserConfigsPreferLocaleUpdateApi(host=self.host, _session=self.session)
        data = UserConfigsPreferLocaleRequestData(preferred_locale=preferred_locale).dict(exclude_none=True)

        response = api.call(data=data)
        return UserConfigsPreferLocaleResponse.parse_raw(b=response.content)

    def send_otp(self, domain: str = "login"):
        api = UserPhoneSendOtpApi(host=self.host, _session=self.session)
        data = UserPhoneSendOtpRequestData(domain=domain).dict(exclude_none=True)

        response = api.call(data=data)
        return UserPhoneSendOtpResponse.parse_raw(b=response.content)

    def verify_otp(self, phone_otp: str):
        api = UserPhoneVerifyOtpApi(host=self.host, _session=self.session)
        data = UserPhoneVerifyOtpRequestData(phone_otp=phone_otp).dict(exclude_none=True)

        response = api.call(data=data)
        return UserPhoneVerifyOtpResponse.parse_raw(b=response.content)

    def verify_passcode(self, passcode: str):
        api = UserPasscodeVerifyApi(host=self.host, _session=self.session)
        data = UserPasscodeVerifyRequestData(passcode=passcode).dict(exclude_none=True)

        response = api.call(data=data)
        return UserPasscodeVerifyResponse.parse_raw(b=response.content)

    def user_show(self):
        api = UserShowApi(host=self.host, _session=self.session)

        response = api.call()
        return UserShowResponse.parse_raw(b=response.content)

    def user_create_phone_number(self) -> UserCreatePhoneResponse:
        api = UserCreatePhoneNumberApi(host=self.host, _session=self.session)

        response = api.call()
        return UserCreatePhoneResponse.parse_raw(b=response.content)

    def user_create_email(self) -> UserCreateEmailResponse:
        api = UserCreateEmailApi(host=self.host, _session=self.session)

        response = api.call()
        return UserCreateEmailResponse.parse_raw(b=response.content)

    def user_update_email(self, email: str, token: str) -> UserUpdateEmailResponse:
        api = UserUpdateEmailApi(host=self.host, _session=self.session)

        data = UserUpdateEmailRequestData(email=email, token=token).dict(exclude_none=True)
        response = api.call(data=data)
        return UserUpdateEmailResponse.parse_raw(b=response.content)

    def user_input_referral_code(self, code: str) -> UserInputReferralCodeResponse:
        api = UserInputReferralCodeApi(host=self.host, _session=self.session)

        data = UserInputReferralCodeRequestData(code=code).dict(exclude_none=True)
        response = api.call(data=data)
        return UserInputReferralCodeResponse.parse_raw(b=response.content)

    def claim_referral_code(self, code: str) -> UserClaimReferralCodeResponse:
        api = UserClaimReferralCodeApi(host=self.host, _session=self.session)

        data = UserClaimReferralCodeReqeustData(code=code).dict(exclude_none=True)
        response = api.call(data=data)
        return UserClaimReferralCodeResponse.parse_raw(b=response.content)

    def passcode_forgot_init(self) -> PasscodeResetInAppInitResponse:
        api = PasscodeResetInAppInitApi(host=self.host, _session=self.session)

        response = api.call()
        return PasscodeResetInAppInitResponse.parse_raw(b=response.content)

    def passcode_forgot_create(self, phone_otp: str, dob: str) -> PasscodeResetInAppCreateResponse:
        api = PasscodeRestInAppCreateApi(host=self.host, _session=self.session)
        data = PasscodeResetInAppCreateRequestData(phone_otp=phone_otp, dob=dob).dict(exclude_none=True)

        response = api.call(data=data)
        return PasscodeResetInAppCreateResponse.parse_raw(b=response.content)

    def passcode_forgot_reset(self, passcode: str, confirmation_token: str) -> PasscodeResetInAppResetResponse:
        api = PasscodeRestInAppResetApi(host=self.host, _session=self.session)
        data = PasscodeResetInAppResetRequestData(
            passcode=passcode,
            confirmation_token=confirmation_token,
        ).dict(exclude_none=True)

        response = api.call(data=data)
        return PasscodeResetInAppResetResponse.parse_raw(b=response.content)
