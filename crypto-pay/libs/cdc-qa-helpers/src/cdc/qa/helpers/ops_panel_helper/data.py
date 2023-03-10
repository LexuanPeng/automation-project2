"""
These are the user feature flags available currently and hardcoded to class `UserFeatureFlag` to allow IDE
suggests the values of user feature flags.

Any new user feature flags are needed to be added here. List of available user feature flags can be called out in
rails console:

    ```
    all_features = []
    UserFeature.constants.each do |feature_sub_class|
      clz = "UserFeature::#{feature_sub_class}".constantize
      clz.constants.each do |c|
        all_features << clz.const_get(c)
      end
    end
    puts all_features
    ```

"""

from enum import unique, Enum, auto


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


@unique
class UserTag(AutoName):
    phone_updated = auto()
    new_users_cc_fees_waived = auto()
    pending_account_closure_banned_us_state = "pending_account_closure:banned_us_state"
    tmx = auto()
    tmx_canary = "tmx-canary"


@unique
class UserFeatureFlag(AutoName):
    pos_pay_enabled = auto()
    QA_CA_DCBANK_APPLICATION_MOCK_JUMIO_ADDRESS = "QA:CA_DCBANK_APPLICATION:MOCK_JUMIO_ADDRESS"
    auto_kyced_true = "auto_kyced: true"
    council_node_enabled = auto()
    crypto_to_van_enabled = auto()
    ach_withdrawal_override_minimum_amount = auto()
    ach_withdrawal_enabled = auto()
    crypto_credit_enabled = auto()
    CARD_FORCE_FREEZE = "CARD:FORCE_FREEZE"
    l10n_enabled = auto()
    viban_withdrawal_enabled = auto()
    QA_VIBAN_UNLIMITED_WITHDRAWAL_COUNT = "QA:VIBAN:UNLIMITED_WITHDRAWAL_COUNT"
    bank_transfer_enabled = auto()
    swift_withdrawal_enabled = auto()
    usd_swift_enabled = auto()
    swift_enabled = auto()
    uk_fps_withdrawal_enabled = auto()
    uk_fps_enabled = auto()
    QA_RESIDENTIAL_ADDRESS_MOCK_JUMIO_CAN_ADDRESS = "QA:RESIDENTIAL_ADDRESS:MOCK_JUMIO_CAN_ADDRESS"
    QA_RESIDENTIAL_ADDRESS_MOCK_JUMIO_AUS_ADDRESS = "QA:RESIDENTIAL_ADDRESS:MOCK_JUMIO_AUS_ADDRESS"
    aud_wallet_withdrawal_enabled = auto()
    aud_wallet_deposit_enabled = auto()
    gift_card_enabled = auto()
    referral_v3_enabled = auto()
    QA_VAN_FAIL = "QA:VAN:FAIL"
    ach_van_top_up_us_card_enabled = auto()
    QA_VAN_HAPPY_CUSTOMER = "QA:VAN:HAPPY_CUSTOMER"
    QA_VAN_CRITICAL_ERROR = "QA:VAN:CRITICAL_ERROR"
    QA_VAN_ADDRESS_PROOF_REQUIRED = "QA:VAN:ADDRESS_PROOF_REQUIRED"
    ach_enabled = auto()
    us_card_application_enabled = auto()
    card_tab_export_enabled = auto()
    mobile_airtime_enabled = auto()
    ca_interac_etransfer_deposit_enabled = auto()
    ca_interac_etransfer_withdrawal_enabled = auto()
    app_review_prompt_enabled = auto()
    us_wire_transfer_enabled = auto()
    purchase_authorize_transaction = "purchase:authorize_transaction"
    xfers_buy_enabled = auto()
    xfers_sell_enabled = auto()
    xfers_enabled = auto()
    pnl_overview_enabled = auto()
    portfolio_details_enabled = auto()
    portfolio_tracker_enabled = auto()
    crypto_earn_enabled = auto()
    QA_SIFT_DOWN = "QA:SIFT:DOWN"
    QA_SIFT_PAYMENT_ABUSE_SCORE_OVER_90 = "QA:SIFT:PAYMENT_ABUSE_SCORE_OVER_90"
    QA_SIFT_ACCOUNT_ABUSE_SCORE_OVER_90 = "QA:SIFT:ACCOUNT_ABUSE_SCORE_OVER_90"
    supercharger_disabled = auto()
    crypto_currency_internal_testing = "crypto_currency:internal_testing"
    crypto_currency_test_new_network = "crypto_currency:test_new_network"
    device_rooted_lock_enabled = auto()
    app_lock_by_server_enabled = auto()
    red_envelope_disabled = auto()
    red_envelope_enabled = auto()
    usdc_swift_withdrawal_enabled = auto()
    usdc_swift_enabled = auto()
    wirecard_us_top_up_enabled = auto()
    test_ixo_pay_pre_authorize = auto()
    credit_card_paydoo_eanbled = auto()
    credit_card_ixo_pay_enabled = auto()
    credit_card_eps24_eanbled = auto()
    wirecard_sg_top_up_enabled = auto()
    wirecard_eu_top_up_enabled = auto()
    invest_enabled = auto()
    cashback_blacklisted = auto()
    crypto_currency_multiple_networks_enabled = auto()
    us_ach_pull_enabled = auto()
    skip_sms_verification = auto()
    sg_standard_chartered_enabled = auto()
    sg_standard_chartered_withdrawal_enabled = auto()
    br_ted_deposit_enabled = auto()
    br_ted_withdrawal_enabled = auto()
    br_pix_deposit_enabled = auto()
    br_pix_withdrawal_enabled = auto()
    br_doc_deposit_enabled = auto()
    br_cmp_deposit_enabled = auto()
    br_cmp_withdrawal_enabled = auto()
    brl_wallet_deposit_enabled = auto()
    brl_wallet_withdrawal_enabled = auto()
    sepa_enabled = auto()
    ar_debin_enabled = auto()
    ar_debin_withdrawal_enabled = auto()
    bulut_tr_remittance_enabled = auto()
    bulut_tr_fast_enabled = auto()
    bulut_tr_eft_enabled = auto()
    bulut_tr_remittance_withdrawal_enabled = auto()
    bulut_tr_fast_withdrawal_enabled = auto()
    bulut_tr_eft_withdrawal_enabled = auto()
