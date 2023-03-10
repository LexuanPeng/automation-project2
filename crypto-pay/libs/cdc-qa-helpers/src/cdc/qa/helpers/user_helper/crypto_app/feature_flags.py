BASE = [
    "bank_transfer_enabled",
    "crypto_credit_enabled",
    "credit_card_ixo_pay_enabled",
    "crypto_earn_enabled",
    "gift_card_enabled",
    "mobile_airtime_enabled",
    "referral_v3_enabled",
    "swift_enabled",
    "swift_withdrawal_enabled",
    "us_ach_pull_enabled",
    "viban_withdrawal_enabled",
]

AG = BASE + ["usdc_swift_enabled", "usdc_swift_withdrawal_enabled"]

AU = BASE

BR = BASE + [
    "br_cmp_deposit_enabled",
    "br_cmp_withdrawal_enabled",
    "br_doc_deposit_enabled",
    "br_pix_deposit_enabled",
    "br_pix_withdrawal_enabled",
    "br_ted_deposit_enabled",
    "br_ted_withdrawal_enabled",
    "brl_wallet_deposit_enabled",
    "brl_wallet_withdrawal_enabled",
]

CA = BASE + ["ca_interac_etransfer_deposit_enabled", "ca_interac_etransfer_withdrawal_enabled"]

MALTA = BASE + ["sepa_enabled"]

SG = BASE + [
    "sepa_enabled",
    "usdc_swift_enabled",
    "usdc_swift_withdrawal_enabled",
    "xfers_buy_enabled",
    "xfers_enabled",
    "xfers_sell_enabled",
]

TK = BASE + [
    "bulut_tr_eft_enabled",
    "bulut_tr_eft_withdrawal_enabled",
    "bulut_tr_fast_enabled",
    "bulut_tr_fast_withdrawal_enabled",
    "bulut_tr_remittance_enabled",
    "bulut_tr_remittance_withdrawal_enabled",
    "sepa_enabled",
]

UK = BASE + [
    "sepa_enabled",
    "uk_fps_enabled",
    "uk_fps_withdrawal_enabled",
    "usdc_swift_enabled",
    "usdc_swift_withdrawal_enabled",
]

US = BASE + ["sepa_enabled"]
