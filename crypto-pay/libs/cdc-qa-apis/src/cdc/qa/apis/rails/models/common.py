from datetime import datetime
from decimal import Decimal

from . import FrozenBaseModel
from typing import Optional, List, Union


class User(FrozenBaseModel):
    class Card(FrozenBaseModel):
        nature: Optional[str]
        lockable: bool
        changeable: bool

    class Identity(FrozenBaseModel):
        verification: Optional[str]
        feedback_to_user: Optional[str]

    uuid: Optional[str]
    name: Optional[str]
    email: Optional[str]
    email_confirmed_at: Optional[str]
    phone: Optional[str]
    phone_confirmed_at: Optional[str]
    unconfirmed_phone: Optional[str]
    should_show_app_review_prompt: Optional[bool]
    referrer_id: Optional[str]
    referral_url: Optional[str]
    local_currency: Optional[str]
    card_type: Optional[str]
    disable_card_picking: Optional[bool]
    region: Optional[str]
    card_stage: Optional[str]
    invest_stage: Optional[str]
    terms_of_service: Optional[bool]
    terms_of_service_accepted_at: Optional[str]
    iban_terms_accepted_at: Optional[str]
    van_terms_accepted_at: Optional[str]
    card_terms_accepted_at: Optional[str]
    newsletters_subscribed_at: Optional[str]
    phone_country: Optional[str]
    crypto_enabled: Optional[bool]
    fiat_enabled: Optional[bool]
    invest_enabled: Optional[bool]
    pay_enabled: Optional[bool]
    crypto_credit_enabled: Optional[bool]
    card_application_enabled: Optional[bool]
    bank_transfer_enabled: Optional[bool]
    card_issued: Optional[bool]
    with_passcode: Optional[bool]
    referral_claimed: Optional[bool]
    base_currency: Optional[str]
    payment_currency: Optional[str]
    base_currency_updated: Optional[bool]
    payment_currency_updated: Optional[bool]
    can_be_referred: Optional[bool]
    council_node_enabled: Optional[bool]
    crypto_earn_enabled: Optional[bool]
    us_card_application_enabled: Optional[bool]
    ach_van_top_up_us_card_enabled: Optional[bool]
    gift_card_enabled: Optional[bool]
    price_alert_enabled: Optional[bool]
    automated_market_alert_enabled: Optional[bool]
    export_transactions_enabled: Optional[bool]
    card: Optional[Card]
    us_card_term: Optional[str]
    identity: Optional[Identity]
    courtesies: Optional[list]


class Balance(FrozenBaseModel):
    currency: Optional[str]
    amount: Optional[Decimal]


class Wallet(FrozenBaseModel):
    class Network(FrozenBaseModel):
        name: str
        short_name: str
        network_id: str
        address: str

    currency: str
    balance: Balance
    native_balance: Balance
    available: Balance
    native_available: Balance
    locked: Balance
    native_locked: Balance
    locked_until: Optional[datetime]
    percentage_change: float
    address: Optional[str]
    display_balance: Balance
    display_available: Balance
    display_locked: Balance
    major_wallet: bool
    networks: List[Network]


class Account(FrozenBaseModel):
    id: int
    native_currency: str
    balance: Balance
    native_balance: Balance
    amount_change: Balance
    percentage_change: float
    wallets: List[Wallet]


class Address(FrozenBaseModel):
    address_1: Optional[str]
    address_2: Optional[str]
    city: Optional[str]
    country: Optional[str]
    postcode: Optional[str]
    state_code: Optional[str]
    zip_code: Optional[str]
    province: Optional[str]
    user_kyc_address: Optional[str]


class Quotation(FrozenBaseModel):
    id: str
    from_amount: Balance
    to_amount: Balance
    native_amount: Balance
    amount_in_usd: Balance
    rate: Decimal
    rate_timestamp: int
    expire_at: datetime
    countdown: int
    fee: Balance
    total_amount: Balance
    next_action: Optional[str]
    execute_rate: List[Balance]
    low_liquidity: Optional[bool]
    fee_percentage: Optional[float]
    to_wallet_name: Optional[str]
    initial_to_amount: Optional[Balance]


class TransferUser(FrozenBaseModel):
    name: Optional[str]
    phone: Optional[str]
    id: Optional[int]


class Transaction(FrozenBaseModel):
    class Meta(FrozenBaseModel):
        class WithdrawTo(FrozenBaseModel):
            bank_name: Optional[str]
            viban_type: str
            identifier_type: Optional[str]
            account_holder_name: str
            masked_identifier_value: str
            external_account_reference: Optional[str]

        class Fee(FrozenBaseModel):
            name: str
            amount: Balance

        class TransactionDetails(FrozenBaseModel):
            class BankDetails(FrozenBaseModel):
                bank_name: Optional[str]
                masked_account_identifier_value: str

            sender: BankDetails

        purchase_id: Optional[str]
        fee_amount: Optional[Balance]
        fee_percentage: Optional[float]
        initial_to_amount: Optional[Balance]
        withdrawal_id: Optional[str]
        withdraw_to: Optional[WithdrawTo]
        fees: Optional[List[Fee]]
        vendor_id: Optional[str]
        payment_network: Optional[str]
        review_time_description: Optional[str]
        crypto_fiat_transaction_id: Optional[str]
        bank_transfer_time_description: Optional[str]
        receivable_amount: Optional[Balance]
        transaction_details: Optional[TransactionDetails]
        crypto_fiat_sender_id: Optional[str]
        crypto_deposit_s: Optional[str]
        crypto_deposit_source_type: Optional[str]

    id: Union[int, str]
    context: str
    nature: str
    kind: Optional[str]
    description: str
    rate: Decimal
    rate_desc: Optional[str]
    amount: Balance
    to_amount: Optional[Balance]
    native_amount: Balance
    native_currency: Optional[str]
    note: Optional[str]
    address: Optional[str]
    status: str
    created_at: str
    updated_at: str
    meta: Optional[Meta]
    fee: Optional[Balance]
    execute_rate: Optional[List[Balance]]
    user_uuid: Optional[str]
    to_user: Optional[TransferUser]
    from_user: Optional[TransferUser]


class RiskAssessments(FrozenBaseModel):
    choice: str
    id: str


class RiskAssessmentsAnswer(FrozenBaseModel):
    class Answer(FrozenBaseModel):
        class Choice(FrozenBaseModel):
            key: str
            text: str
            translation_key: str

        id: str
        title: str
        subtitle: str
        title_translation_key: str
        subtitle_translation_key: str
        status: str
        choices: List[Choice]

    risk_assessments: List[Answer]
