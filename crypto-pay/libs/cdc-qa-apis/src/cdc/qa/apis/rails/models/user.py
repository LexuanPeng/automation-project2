from . import FrozenBaseModel, RailsEncryptedPasscodeRequest, RailsResponse
from pydantic import Field
from .common import User, Balance
from typing import Optional


# --------------------------------- UserAuth --------------------------------- #
class UserAuthRequestData(FrozenBaseModel):
    email: str = Field()


class UserAuthResponse(RailsResponse):
    class UserAuthResponseUser(FrozenBaseModel):
        email: str = Field()

    user: UserAuthResponseUser = Field()


# ------------------------------ UserPhoneSendOtp ----------------------------- #
class UserPhoneSendOtpRequestData(FrozenBaseModel):
    domain: str = Field(default="login")


class UserPhoneSendOtpResponse(RailsResponse):
    pass


# ------------------------------ UserPhoneSendOtp ----------------------------- #
class UserPhoneVerifyOtpRequestData(FrozenBaseModel):
    phone_otp: str = Field()


class UserPhoneVerifyOtpResponse(RailsResponse):
    is_valid_otp: bool = Field()


# ------------------------------ UserPhoneUpdate ----------------------------- #
class UserPhoneUpdateRequestData(FrozenBaseModel):
    phone: str = Field()
    token: Optional[str]


class UserPhoneUpdateResponse(RailsResponse):
    user: User = Field()


# ------------------------------ UserPhoneVerify ----------------------------- #
class UserPhoneVerifyRequestData(FrozenBaseModel):
    otp: str = Field()


class UserPhoneVerifyResponse(RailsResponse):
    user: User = Field()


# ------------------------------ UserTermsUpdate ----------------------------- #
class UserTermsUpdateRequestData(FrozenBaseModel):
    terms_of_service: bool = Field()


class UserTermsUpdateResponse(RailsResponse):
    user: User = Field()


# ------------------------------ UserNewslettersUpdate ----------------------- #
class UserNewslettersUpdateRequestData(FrozenBaseModel):
    subscribe_newsletters: bool = Field()


class UserNewslettersUpdateResponse(RailsResponse):
    user: User = Field()


# ------------------------------ UserNameUpdate ------------------------------ #
class UserNameUpdateRequestData(FrozenBaseModel):
    name: str = Field()


class UserNameUpdateResponse(RailsResponse):
    user: User = Field()


# ------------------------------ UserPasscodeUpdate -------------------------- #
class UserPasscodeUpdateRequestData(RailsEncryptedPasscodeRequest):
    current_passcode: Optional[str]


class UserPasscodeUpdateResponse(RailsResponse):
    class UserPasscodeUpdateResponseUser(FrozenBaseModel):
        email: str = Field()

    user: UserPasscodeUpdateResponseUser = Field()


# ------------------------------ UserPasscodeVerify -------------------------- #
class UserPasscodeVerifyRequestData(RailsEncryptedPasscodeRequest):
    pass


class UserPasscodeVerifyResponse(UserPasscodeUpdateResponse):
    pass


# UserPaymentCurrencyUpdate
class UserPaymentCurrencyUpdateRequestData(FrozenBaseModel):
    payment_currency: str = Field()


class UserPaymentCurrencyUpdateResponse(RailsResponse):
    user: User = Field()


# ------------------------------ UserConfig ------------------------------ #
class UserConfig(FrozenBaseModel):
    outgoing_sms_permitted: bool
    preferred_locale: str
    super_menu_shortcuts_enabled: bool
    preferred_app_default_homepage: str
    ios_activity_tracking_enabled: Optional[bool]
    android_activity_tracking_enabled: Optional[bool]
    pay_merchant_refund_currency: Optional[str]


class UserConfigResponse(RailsResponse):
    user_config: UserConfig = Field()


# ------------------------------ UserConfigsSupermenuShortcutsEnabledUpdate ------------------------------ #
class UserConfigsSupermenuShortcutsEnabledUpdateRequestData(FrozenBaseModel):
    super_menu_shortcuts_enabled: bool = Field()


class UserConfigsSupermenuShortcutsEnabledUpdateResponse(RailsResponse):
    user_config: UserConfig = Field()


# ------------------------------ UserPreferLocale------------------------------ #
class UserConfigsPreferLocaleRequestData(FrozenBaseModel):
    preferred_locale: str = Field()


class UserConfigsPreferLocaleResponse(RailsResponse):
    user_config: UserConfig = Field()


# ------------------------------ UserShow ------------------------------ #
class UserShowResponse(RailsResponse):
    user: User = Field()


# Create phone number
class UserCreatePhoneResponse(RailsResponse):
    pass


# Create and update email
class UserCreateEmailResponse(RailsResponse):
    pass


class UserUpdateEmailRequestData(FrozenBaseModel):
    email: str
    token: str


class UserUpdateEmailResponse(RailsResponse):
    pass


# User referral Code
class UserInputReferralCodeRequestData(FrozenBaseModel):
    code: str


class UserInputReferralCodeResponse(RailsResponse):
    pass


class UserClaimReferralCodeReqeustData(UserInputReferralCodeRequestData):
    pass


class UserClaimReferralCodeResponse(RailsResponse):
    class Subscription(FrozenBaseModel):
        class Reward(FrozenBaseModel):
            class CashBack(FrozenBaseModel):
                amount: Balance
                earn_at: Optional[str]
                referral_count: Optional[int]
                is_locked: Optional[bool]

            wallet_cashback: CashBack
            card_cashback: CashBack
            card_reimbursement: CashBack
            commission: CashBack
            gift: CashBack
            referral_bonus: CashBack
            council_node_rewards: CashBack
            pay_rewards: CashBack
            gift_card_rewards: CashBack
            mobile_airtime_rewards: CashBack
            transfer_cashback: CashBack
            pay_checkout_rewards: CashBack
            total_earned: CashBack
            pos_pay_rewards: CashBack

        class Benefits(FrozenBaseModel):
            wallet_cashback_percentage: str
            referral_commission_percentage: str
            referral_limit: int
            referral_quota: int
            referral_gift: Balance
            card_purchase_cashback_percentage: str

        enabled: bool
        plan: str
        rewards: Reward
        benefits: Benefits
        lock_until: Optional[str]

    subscription: Subscription


# Passcode Reset init in app
class PasscodeResetInAppInitResponse(RailsResponse):
    class Allowed(FrozenBaseModel):
        allowed: bool

    reset_in_app: Allowed


# Passcode create in app
class PasscodeResetInAppCreateRequestData(FrozenBaseModel):
    phone_otp: str
    dob: str


class PasscodeResetInAppCreateResponse(RailsResponse):
    class Meta(FrozenBaseModel):
        app_locked: bool
        app_lock_expires_at: str
        lock_duration_in_minutes: int
        remaining_number_of_attempts: int
        maximum_number_of_verification_attempts: int

    meta: Optional[Meta]


# Passcode Reset in app
class PasscodeResetInAppResetRequestData(RailsEncryptedPasscodeRequest):
    confirmation_token: str


class PasscodeResetInAppResetResponse(RailsResponse):
    pass
