"""
These are the global flags and internal testers lists available currently and hardcoded to allow IDE suggests the
values of user feature flags.

Any new global flags and internal testers lists are needed to be added here.
"""

from enum import Enum, unique, auto


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


@unique
class GlobalFlag(AutoName):
    qa_fake_i2c_top_up = auto()
    us_virtual_card_application_enabled = auto()
    eu_virtual_card_application_enabled = auto()
    au_card_application_enabled = auto()
    au_card_application_popup_enabled = auto()
    recurring_buy_enabled = auto()
    skip_crypto_withdrawal_risk_control = auto()
    crypto_login_phone_otp_verification_enabled = auto()
    crypto_transfer_request_mandatory_totp_enabled = auto()
    crypto_transfer_request_phone_otp_enabled = auto()
    gift_card_mandatory_totp_status_check_enabled = auto()
    gift_card_mandatory_totp_validation_enabled = auto()
    mobile_airtime_mandatory_totp_status_check_enabled = auto()
    mobile_airtime_mandatory_totp_validation_enabled = auto()
    ca_interac_etransfer_deposit_enabled = auto()
    uk_fps_enabled = auto()
    uk_fps_withdrawal_enabled = auto()
    brl_wallet_deposit_enabled = auto()
    brl_wallet_withdrawal_enabled = auto()
    br_ted_deposit_enabled = auto()
    br_ted_withdrawal_enabled = auto()
    br_pix_deposit_enabled = auto()
    br_pix_withdrawal_enabled = auto()
    br_doc_deposit_enabled = auto()
    br_cmp_deposit_enabled = auto()
    br_cmp_withdrawal_enabled = auto()
    aud_wallet_withdrawal_enabled = auto()
    aud_wallet_deposit_enabled = auto()
    sg_standard_chartered_enabled = auto()
    sg_standard_chartered_withdrawal_enabled = auto()
    daily_recurring_buy_enabled = auto()
    crypto_currency_multiple_networks_enabled = auto()
    ars_payment_currency_enabled = auto()
    ar_debin_enabled = auto()
    ar_debin_withdrawal_enabled = auto()
    ca_view_virtual_card_details_enabled = auto()
    ca_virtual_card_issuing_enabled = auto()
    bulut_wallet_deposit_enabled = auto()
    bulut_wallet_withdrawal_enabled = auto()
    bulut_tr_remittance_enabled = auto()
    bulut_tr_fast_enabled = auto()
    bulut_tr_eft_enabled = auto()
    bulut_tr_remittance_withdrawal_enabled = auto()
    bulut_tr_fast_withdrawal_enabled = auto()
    bulut_tr_eft_withdrawal_enabled = auto()
    br_card_application_enabled = auto()
    br_card_application_popup_enabled = auto()
    whitelist_pay_id__passcode_verification_enabled = auto()


@unique
class InternalTestersList(AutoName):
    van_migration_internal_testers = auto()
    us_wire_transfer_internal_testers = auto()
    entity_restrictions_bypass_internal_testers = auto()
    crypto_login_phone_otp_verification_internal_testers = auto()
    qa_sepa_disabled_internal_testers = auto()
    crypto_withdrawal_phone_otp_verification_internal_testers = auto()
    uk_fps_withdrawal_internal_testers = auto()
    fag_internal_testers = auto()
    bulut_qa_skip_tckn_match_users = auto()
    eur_whitelist_internal_testers = auto()
    crypto_earn_flash_apy_internal_testers = auto()


@unique
class USDFiatWalletDepositMethod(AutoName):
    van = auto()
    us_wire_transfer = auto()


@unique
class XfersConnectState(AutoName):
    pending_xfers_verify = auto()
    pending_review = auto()
    activated = auto()
    disconnected = auto()
    rejected = auto()


@unique
class DobVerificationSettings(AutoName):
    maximum_number_of_verification_attempts = auto()
    lock_duration_in_minutes = auto()
