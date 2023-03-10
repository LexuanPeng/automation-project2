import uuid
from datetime import datetime, date
from decimal import Decimal
from typing import List, Optional, Union

from cdc.qa.apis.rails import RailsResponse
from cdc.qa.apis.rails.models import FrozenBaseModel, RailsEncryptedPasscodeRequest
from cdc.qa.apis.rails.models.common import Address, Balance, Quotation, Transaction

from pydantic import Field, AnyHttpUrl


# CryptoFiatDepositMethodsTermsAccept
class CryptoFiatDepositMethodsTermsAcceptRequestData(FrozenBaseModel):
    term_id: str = Field()
    currency: str = Field()
    deposit_methods: List[str] = Field()


class CryptoFiatDepositMethodsShowQueryParams(FrozenBaseModel):
    currency: str = Field()


class CryptoFiatDepositMethodsShowPathParams(FrozenBaseModel):
    currency: str = Field()


class FiatBankAccountsPathParams(FrozenBaseModel):
    currency: str = Field()
    payment_network: Optional[str]


class FiatDeleteBankAccountsPathParams(FrozenBaseModel):
    id: str = Field()


class CryptoFiatDepositMethodsShowResponse(RailsResponse):
    class DepositMethod(FrozenBaseModel):
        class BankDetail(FrozenBaseModel):
            key: str
            translation_key: str
            value: Optional[str]

        deposit_method: str
        user_uuid: str
        currency: str
        bank_details: List[BankDetail]
        meta: Optional[str]
        limits: Optional[str]
        fees: Optional[str]
        deposit_method_name_translation_key: Optional[str]
        deposit_method_description_translation_key: Optional[str]

    deposit_methods: List[DepositMethod] = Field()


class CryptoFiatDepositMethodsTermsAcceptResponse(RailsResponse):
    class Term(FrozenBaseModel):
        user_uuid: str
        viban_type: str
        currency: str
        term_id: str
        created_at: datetime
        additional_information: Optional[str]
        version: int

    accepted_terms: List[Term] = Field()


# USVanApplicationAddressUpdate
class USVanApplicationAddressUpdateRequestData(FrozenBaseModel):
    address: Address = Field()


class USVanApplicationAddressUpdateResponse(RailsResponse):
    address: Address = Field()


# USVanApplicationUpdate
class USVanApplicationUpdateRequestData(FrozenBaseModel):
    ssn9: str = Field()


class USVanApplicationUpdateResponse(RailsResponse):
    class Retry(FrozenBaseModel):
        attempted: int
        remaining_attempts: int

    state: str = Field()
    resubmit_fields: List[str] = Field()
    retry: Retry = Field()


class ACHBankAccount(FrozenBaseModel):
    id: str
    bank_name: str
    masked_identifier_value: str
    is_withdrawable: bool
    created_at: datetime
    updated_at: datetime


class Withdrawal(FrozenBaseModel):
    id: str
    passcode_required: bool
    passcode_verified: bool
    otp_required: bool
    otp_required: bool
    amount: Balance
    native_amount: Balance
    fee_amount: Balance
    fee_recipient: str
    total_withdrawal_amount: Balance
    withdrawal_method: str
    created_at: str
    updated_at: str
    bank_account: ACHBankAccount


class Meta(FrozenBaseModel):
    class Navigation(FrozenBaseModel):
        current: str
        next: str

    navigation: Navigation


# ACHWithdrawalBankAccountsCreate
class ACHWithdrawalBankAccountsCreateRequestData(FrozenBaseModel):
    institution_name: str = Field()
    plaid_public_token: str = Field()
    account_id: str = Field()


class ACHWithdrawalBankAccountsCreateResponse(RailsResponse):
    bank_account: ACHBankAccount = Field()


# ACHWithdrawalBankAccounts
class ACHWithdrawalBankAccountsResponse(RailsResponse):
    bank_accounts: List[ACHBankAccount] = Field()


# ACHWithdrawalWithdrawalCreate
class ACHWithdrawalWithdrawalCreateRequestData(FrozenBaseModel):
    bank_account_id: str = Field()
    amount: Decimal = Field()


class ACHWithdrawalWithdrawalCreateResponse(RailsResponse):
    withdrawal: Withdrawal = Field()
    meta: Meta = Field()


# ACHWithdrawalWithdrawalVerifyPasscode
class ACHWithdrawalWithdrawalVerifyPasscodeRequestData(RailsEncryptedPasscodeRequest):
    withdrawal_id: str = Field()


class ACHWithdrawalWithdrawalVerifyPasscodeResponse(RailsResponse):
    withdrawal: Withdrawal = Field()
    meta: Meta = Field()


# XfersTNCCreate
class XfersTNCCreateRequestData(FrozenBaseModel):
    payment_currency: str = Field(default="SGD")


class XfersTNCCreateResponse(RailsResponse):
    pass


# XfersConnect
class XfersConnectRequestData(FrozenBaseModel):
    otp: str = Field(default="000000")


class XfersConnectResponse(RailsResponse):
    class Account(FrozenBaseModel):
        class Details(FrozenBaseModel):
            id: str
            available_balance: str
            ledger_balance: str
            default_account_id: str
            bank_transfer_rates: str
            bank_transfer_fees: str
            full_name: str
            first_name: str
            last_name: str
            date_of_birth: date
            gender: str
            email: str
            unconfirmed_email: str
            country: str
            state: str
            city: str
            nationality: str
            address_line_1: str
            address_line_2: str
            postal_code: str
            identity_no: str
            phone_no: str
            bank_accounts: List[str]
            annual_income: str
            account_locked: bool
            kyc_limit_remaining: str
            meta_data: str
            account_type: str
            wallet_name: str
            wallet_id: int
            gauth_enabled: bool
            kyc_verified: bool
            kyc_verified_date: Optional[date]
            account_fully_verified: bool
            kyc_rejected_reason: Optional[str]
            kyc_information_edit_allowed: bool
            kyc_information_verifying: bool
            storage_limit_exceeded: bool
            verification_status: str
            identification_status: str
            id_front_url: str
            id_back_url: str
            proof_of_address_url: str
            signature_url: str
            country_of_birth: str
            nric_issue_date: str
            nric_expiry_date: str
            nric_type: str
            is_myinfo_flow: bool
            annual_income_range: str
            occupation: str
            employment_sector: str
            employer: Optional[str]
            expected_transaction_amount: str
            expected_total_transaction: str
            expected_transaction_frequency: str
            id_front_uploaded: bool
            id_back_uploaded: bool
            selfie_uploaded: bool
            proof_of_address_uploaded: bool

        id: str
        user_uuid: str
        state: str
        account_holder_name: str
        phone: str
        available_balance: Balance
        buy_fee_percentage: str
        sell_fee_percentage: str
        sign_up_url: AnyHttpUrl
        details: Details
        pending_balance: Balance
        total_balance: Balance
        native_available_balance: Balance


# CryptoFiatDepositMethodsCreate
class CryptoFiatDepositMethodsCreateRequestData(FrozenBaseModel):
    currency: str = Field()
    deposit_methods: List[str] = Field()


class CryptoFiatDepositMethodsCreateResponse(RailsResponse):
    class DepositMethod(FrozenBaseModel):
        class BankDetail(FrozenBaseModel):
            key: str
            translation_key: str
            value: Optional[str]

        deposit_method: str
        user_uuid: str
        currency: str
        bank_details: List[BankDetail]
        meta: Optional[str]

    deposit_methods: List[DepositMethod] = Field()


# Common Fiat Purchases
class CommonFiatPurchasesQuotationCreateRequest(FrozenBaseModel):
    to_amount: str = Field()
    from_currency: str = Field()
    to_currency: str = Field()


class CommonFiatPurchasesQuotationCreateResponse(RailsResponse):
    quotation: Quotation = Field()


class CommonFiatPurchasesCreateRequest(RailsEncryptedPasscodeRequest):
    quotation_id: str = Field()


class CommonFiatPurchasesCreateResponse(RailsResponse):
    transaction: Transaction = Field()


# Common Fiat Sells
class CommonFiatSellQuotationCreateRequest(FrozenBaseModel):
    from_amount: str = Field()
    from_currency: str = Field()
    to_currency: str = Field()


class CommonFiatSellQuotationCreateResponse(RailsResponse):
    quotation: Quotation = Field()


class CommonFiatSellCreateRequest(RailsEncryptedPasscodeRequest):
    otp: Optional[str] = Field()
    quotation_id: str = Field()


class CommonFiatSellCreateResponse(RailsResponse):
    transaction: Transaction = Field()


# VibanAccountSummary
class VibanAccountSummaryResponse(RailsResponse):
    class Account(FrozenBaseModel):
        class Fees(FrozenBaseModel):
            year_to_date: Balance
            last_month: Balance

        class VibanType(FrozenBaseModel):
            type: str
            name: str
            symbol: str
            currency: str
            state: str
            reactivation_required: Optional[bool]
            amount: Balance
            native_amount: Balance
            enabled_viban_types: Optional[List[str]]

        class VibanBalance(FrozenBaseModel):
            enabled_viban_types: List[str]
            currency: str
            amount: Balance
            native_amount: Balance

        fees: Fees
        balance: Balance
        native_balance: Balance
        viban_types: List[VibanType]
        balances: List[VibanBalance]
        pending_terms: List[str]

    account: Account = Field()


class VibanTermsAcceptRequestData(FrozenBaseModel):
    currency: str = Field()
    viban_type: str = Field()
    term_id: str = Field()


class VibanTermsAcceptResponse(RailsResponse):
    class VibanAcceptedTerm(FrozenBaseModel):
        user_uuid: str
        viban_type: str
        currency: str
        term_id: str
        created_at: str
        additional_information: Optional[str]
        version: int

    viban_accepted_term: VibanAcceptedTerm


# VibanPurchasesQuotationCreate
class VibanPurchasesQuotationCreateRequestData(CommonFiatPurchasesQuotationCreateRequest):
    pass


class VibanPurchasesQuotationCreateResponse(CommonFiatPurchasesQuotationCreateResponse):
    pass


# VibanPurchasesCreate
class VibanPurchasesCreateRequestData(CommonFiatPurchasesCreateRequest):
    pass


class VibanPurchasesCreateResponse(CommonFiatPurchasesCreateResponse):
    pass


# VibanSellQuotationCreate
class VibanSellQuotationCreateRequestData(CommonFiatSellQuotationCreateRequest):
    pass


class VibanSellQuotationCreateResponse(CommonFiatSellQuotationCreateResponse):
    pass


# VibanSellCreate
class VibanSellCreateRequestData(CommonFiatSellCreateRequest):
    pass


class VibanSellCreateResponse(CommonFiatSellCreateResponse):
    pass


class VibanWithdrawalBeneficiary(FrozenBaseModel):
    id: str
    user_uuid: Optional[str]
    viban_type: str
    network_name: str
    currency: Optional[str]
    identifier_type: Optional[str]
    identifier_value: Optional[str]
    masked_identifier_value: str
    account_holder_name: str
    bank_country: Optional[str]
    bank_identifier_type: Optional[str]
    bank_identifier_value: Optional[str]
    bank_name: Optional[str]
    external_account_reference: Optional[str]
    entity_type: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    date_of_birth: Optional[str]
    company_name: Optional[str]
    company_incorporation_number: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    address: Optional[str]
    postcode: Optional[str]
    currency_cloud_sender: Optional[str]
    currency_cloud_beneficiary_id: Optional[str]
    currency_cloud_beneficiary: Optional[str]
    currency_cloud_account_type: Optional[str]
    active: Optional[bool]
    is_visible: Optional[bool]
    created_at: str
    updated_at: str
    phone: Optional[str]
    bank_account_id: Optional[str]
    status: Optional[str]


# VibanWithdrawalBeneficiaries (GET)
class VibanWithdrawalBeneficiariesQueryParams(FrozenBaseModel):
    currency: str = Field()
    viban_type: str = Field()


class VibanWithdrawalBeneficiariesResponse(RailsResponse):
    viban_withdrawal_beneficiaries: List[VibanWithdrawalBeneficiary] = Field()


# VibanWithdrawalBeneficiaries (POST)
class PostVibanWithdrawalBeneficiariesRequestData(FrozenBaseModel):
    bank_name: Optional[str] = Field()
    plaid_public_token: Optional[str] = Field()
    payment_network: str = Field(default="us_ach")
    account_identifier_value: str = Field()
    currency: str = Field(default="USD")
    account_identifier_type: Optional[str] = Field()
    account_holder_name_first_name: Optional[str] = Field()
    account_holder_name_last_name: Optional[str] = Field()
    phone: Optional[str] = Field()


class PostVibanWithdrawalBeneficiariesResponse(RailsResponse):
    viban_withdrawal_beneficiary: VibanWithdrawalBeneficiary = Field()


# VibanWithdrawalOrdersCreate
class VibanWithdrawalOrdersCreateRequestData(FrozenBaseModel):
    beneficiary_id: str = Field()
    amount: str = Field()
    currency: str = Field()
    viban_type: str = Field()
    security_question: Optional[str] = Field()
    security_answer: Optional[str] = Field()


class VibanWithdrawalOrder(FrozenBaseModel):
    class Fee(FrozenBaseModel):
        name: str
        amount: Balance

    id: str
    user_uuid: str
    fee: Optional[Balance]
    fees: List[Fee]
    amount: Balance
    receivable_amount: Balance
    network_name: str
    withdrawal_beneficiary: VibanWithdrawalBeneficiary
    review_time_description: str
    bank_transfer_time_description: str
    security_question: Optional[str]
    security_answer: Optional[str]
    created_at: str
    updated_at: str


class VibanWithdrawalOrdersCreateResponse(RailsResponse):
    viban_withdrawal_order: VibanWithdrawalOrder = Field()


# VibanWithdrawalCreate
class VibanWithdrawalCreateRequestData(RailsEncryptedPasscodeRequest):
    order_id: str = Field()
    otp: str = Field()


class VibanWithdrawalCreateNoOtpRequestData(RailsEncryptedPasscodeRequest):
    order_id: str = Field()


class VibanWithdrawalCreateResponse(RailsResponse):
    class VibanWithdrawal(FrozenBaseModel):
        class Order(FrozenBaseModel):
            class Fee(FrozenBaseModel):
                name: str
                amount: Balance

            id: str
            user_uuid: str
            fee: Optional[Balance]
            fees: List[Fee]
            amount: Balance
            receivable_amount: Balance
            network_name: str
            withdrawal_beneficiary: VibanWithdrawalBeneficiary
            review_time_description: str
            bank_transfer_time_description: str
            security_question: Optional[str]
            security_answer: Optional[str]
            created_at: str
            updated_at: str

        class History(FrozenBaseModel):
            created_at: str
            event_type: str

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

            fees: List[Fee]
            withdraw_to: WithdrawTo
            withdrawal_id: str
            security_answer: Optional[str]
            receivable_amount: Balance
            security_question: Optional[str]
            review_time_description: str
            bank_transfer_time_description: str

        id: str
        user_uuid: str
        order: Order
        status: str
        viban_type: str
        beneficiary: VibanWithdrawalBeneficiary
        amount: Balance
        fee: Balance
        receivable_amount: Balance
        amount_in_usd: str
        history: List[History]
        rejected_at: Optional[str]
        completed_at: Optional[str]
        meta: Meta
        created_at: str
        updated_at: str
        vendor_id: Optional[str]

    viban_withdrawal: VibanWithdrawal = Field()


# XfersAccountShow
class XfersAccountShowResponse(RailsResponse):
    class Account(FrozenBaseModel):
        class Details(FrozenBaseModel):
            id: str
            available_balance: str
            ledger_balance: str
            default_account_id: str
            bank_transfer_rates: str
            bank_transfer_fees: str
            full_name: str
            first_name: str
            last_name: str
            date_of_birth: date
            gender: str
            email: str
            unconfirmed_email: str
            country: str
            state: str
            city: str
            nationality: str
            address_line_1: str
            address_line_2: str
            postal_code: str
            identity_no: str
            phone_no: str
            bank_accounts: List[str]
            annual_income: str
            account_locked: bool
            kyc_limit_remaining: str
            meta_data: str
            account_type: str
            wallet_name: str
            wallet_id: int
            gauth_enabled: bool
            kyc_verified: bool
            kyc_verified_date: Optional[date]
            account_fully_verified: bool
            kyc_rejected_reason: Optional[str]
            kyc_information_edit_allowed: bool
            kyc_information_verifying: bool
            storage_limit_exceeded: bool
            verification_status: str
            identification_status: str
            country_of_birth: str
            nric_issue_date: str
            nric_expiry_date: str
            nric_type: str
            is_myinfo_flow: bool
            annual_income_range: str
            occupation: str
            employment_sector: str
            employer: Optional[str]
            expected_transaction_amount: str
            expected_total_transaction: str
            expected_transaction_frequency: str
            id_front_uploaded: bool
            id_back_uploaded: bool
            selfie_uploaded: bool
            proof_of_address_uploaded: bool

        id: str
        user_uuid: str
        state: str
        account_holder_name: str
        phone: str
        available_balance: Balance
        buy_fee_percentage: str
        sell_fee_percentage: str
        sign_up_url: Optional[AnyHttpUrl]
        details: Details
        pending_balance: Balance
        total_balance: Balance
        native_available_balance: Balance
        max_transaction_amount: Balance

    account: Account = Field()


# XfersPurchaseQuotationCreate
class XfersPurchaseQuotationCreateRequestData(CommonFiatPurchasesQuotationCreateRequest):
    pass


class XfersPurchaseQuotationCreateResponse(CommonFiatPurchasesQuotationCreateResponse):
    pass


# XfersPurchaseCreate
class XfersPurchaseCreateRequestData(CommonFiatPurchasesCreateRequest):
    pass


class XfersPurchaseCreateResponse(CommonFiatPurchasesCreateResponse):
    pass


class XfersSellQuotationCreateRequestData(CommonFiatSellQuotationCreateRequest):
    pass


class XfersSellQuotationCreateResponse(CommonFiatSellQuotationCreateResponse):
    pass


class XfersSellCreateRequestData(CommonFiatSellCreateRequest):
    pass


class XfersSellCreateResponse(CommonFiatSellCreateResponse):
    pass


# FiatWalletsTransactions
class FiatWalletsTransactionsQueryParams(FrozenBaseModel):
    count: int = Field()


class FiatWalletsTransactionsResponse(RailsResponse):
    class Meta(FrozenBaseModel):
        class Pagination(FrozenBaseModel):
            total: int

        pagination: Pagination

    transactions: List[Transaction] = Field()
    meta: Meta = Field()


# Exchanges
class ExchangesQuotationCreateRequest(FrozenBaseModel):
    from_amount: Decimal = Field()
    from_side: str = Field(alias="from")
    to: str = Field()


class ExchangesQuotationCreateResponse(RailsResponse):
    quotation: Quotation = Field()


# CA DcBank
class DcBankGetOccupationResponse(RailsResponse):
    class Occupations(FrozenBaseModel):
        require_specification: bool
        key: str
        translation_key: str

    occupations: List[Occupations] = Field()


class DcBankSelectOccupationRequestData(FrozenBaseModel):
    class Occupation(FrozenBaseModel):
        require_specification: bool
        key: str
        specification: Optional[str]
        translation_key: str

    occupation: Occupation = Field()


class DcBankSelectOccupationResponse(RailsResponse):
    pass


class DcBankGetSourceOfFundsResponse(RailsResponse):
    class SourceOfFunds(FrozenBaseModel):
        key: str
        translation_key: str

    source_of_funds: List[SourceOfFunds] = Field()


class DcBankSelectSourceOfFundsRequestData(FrozenBaseModel):
    source_of_funds: List[str] = Field()


class DcBankSelectSourceOfFundsResponse(RailsResponse):
    class SourceOfFunds(FrozenBaseModel):
        key: str
        translation_key: str

    source_of_funds: List[SourceOfFunds] = Field()


class DcBankGetAddressResponse(RailsResponse):
    class Address(FrozenBaseModel):
        id: Optional[Union[str, int]]
        user_id: Optional[Union[str, int]]
        address_1: Optional[str]
        address_2: Optional[str]
        city: Optional[str]
        country: Optional[str]
        postcode: Optional[str]
        proof_scan_reference: Optional[str]
        proof_scan_provider: Optional[str]
        verification: Optional[str]
        created_at: Optional[str]
        updated_at: Optional[str]
        state_code: Optional[str]
        zip_code: Optional[str]
        province: Optional[str]
        log_data: Optional[str]

    class Provinces(FrozenBaseModel):
        key: str
        translation_key: str

    address: Address = Field()
    province_key: Optional[str] = Field()
    provinces: List[Provinces] = Field()
    address_submission_skippable: bool = Field()


class DcBankSubmitAddressRequestData(FrozenBaseModel):
    class Address(FrozenBaseModel):
        address_1: str
        city: str
        country: str
        province: str
        zip_code: str

    address: Address = Field()
    province_key: str = Field()


class DcBankSubmitAddressResponse(RailsResponse):
    class Address(FrozenBaseModel):
        id: Optional[str]
        address_1: str
        address_2: Optional[str]
        city: str
        country: str
        postcode: Optional[str]
        proof_scan_reference: Optional[str]
        proof_scan_provider: Optional[str]
        verification: str
        created_at: Optional[str]
        updated_at: Optional[str]
        state_code: Optional[str]
        zip_code: str
        province: str
        log_data: Optional[str]

    address: Address = Field()
    province_key: str = Field()
    address_submission_skippable: bool = Field()


class DcBankSubmitApplicationResponse(RailsResponse):
    class CaDcbankApplication(FrozenBaseModel):
        class Retry(FrozenBaseModel):
            attempted: int
            remaining_attempts: int

        state: str
        resubmit_fields: List[str]
        retry: Retry

    ca_dcbank_application: CaDcbankApplication = Field()


class CADFiatDepositByReferenceNumberOverviewResponse(RailsResponse):
    class Overview(FrozenBaseModel):
        current_deposit_quota: int
        is_daily_deposit_limit_exceeded: bool
        is_monthly_deposit_limit_exceeded: bool

    overview: Overview = Field()


class CADFiatDepositCreateRequestData(FrozenBaseModel):
    reference_number: str = Field()


class CADFiatDepositCreateResponse(RailsResponse):
    current_deposit_quota: int = Field()


class DcBankApplicationAddressProofRequestData(FrozenBaseModel):
    proof_scan_reference: str = Field(default=uuid.uuid4().__str__())


class DcBankApplicationAddressProofResponse(RailsResponse):
    address_proof: str


# UK FPS
class UKFPSSubmitAddressRequestData(FrozenBaseModel):
    class Address(FrozenBaseModel):
        postcode: str
        address_3: str
        province: Optional[str]
        address_2: Optional[str]
        city: str
        country: str
        address_1: str

    payment_network: str = Field()
    vendor_id: str = Field()
    address: Address = Field()


class UKFPSSubmitAddressResponse(RailsResponse):
    pass


class UKFPSSubmitAddressProofRequestData(FrozenBaseModel):
    proof_scan_reference: str = Field(default=uuid.uuid4().__str__())
    payment_network: str = Field(default="uk_fps")
    vendor_id: str = Field(default="bcb")


class UKFPSSubmitAddressProofResponse(RailsResponse):
    address_proof: str


# BRL Fiat
# BancoPluralApplication
class BancoPluralApplicationResponse(RailsResponse):
    class BancoPluralApplication(FrozenBaseModel):
        id: str
        user_uuid: str
        state: str
        is_triggered_by_card_flow: bool
        created_at: datetime
        updated_at: datetime

    banco_plural_application: BancoPluralApplication = Field()


# BancoPluralApplicationCPF
class BancoPluralApplicationCPFData(FrozenBaseModel):
    cpf: str
    is_triggered_by_card_flow: bool


class BancoPluralApplicationCPFResponse(RailsResponse):
    pass


# BancoPluralApplicationAddress
class BancoPluralApplicationAddressData(FrozenBaseModel):
    class Address(FrozenBaseModel):
        complement: str
        county: str
        neighborhood: str
        state_code: str
        street: str
        street_number: str
        zip_code: str

    address: Address = Field()


class BancoPluralApplicationAddressResponse(RailsResponse):
    pass


# Fiat Application (SG Fast and ARS Debin)
class FiatApplicationRequestData(FrozenBaseModel):
    currency: str = Field()


class BankAccount(FrozenBaseModel):
    bank_country: Optional[str]
    bank_identifier_type: Optional[str]
    account_identifier_type: Optional[str]
    authenticated_by: Optional[str]
    auto_approved: Optional[bool]

    account_identifier_value: Optional[str]
    bank_account_holder_name: Optional[str]
    bank_city: Optional[str]
    bank_identifier_value: Optional[str]
    bank_name: Optional[str]


class ApplicationAddress(FrozenBaseModel):
    postcode: Optional[str]
    zipcode: Optional[str]
    address_3: Optional[str]
    province: Optional[str]
    address_2: Optional[str]
    city: Optional[str]
    country: str
    address_1: Optional[str]


class Application(FrozenBaseModel):
    class Details(FrozenBaseModel):
        class Terms(FrozenBaseModel):
            link: str
            version: Optional[int]
            created_at: Optional[str]

        class Deposit(FrozenBaseModel):
            bank_account_id: Optional[str]

        terms: Optional[Terms]
        deposit: Optional[Deposit]
        bank_account: Optional[BankAccount]
        address: Optional[ApplicationAddress]

    class Overview(FrozenBaseModel):
        step_type: str
        step_action: Optional[str]
        step_status: str
        step_errors: List[Optional[str]]

    id: str
    user_uuid: str
    status: str
    service_account_id: Optional[str]
    verification_step: str
    details: Optional[Details]
    overview: Optional[List[Overview]]
    created_at: str
    updated_at: str
    currency: Optional[str]


class FiatApplicationResponse(RailsResponse):
    application: Application = Field()


class FiatApplicationTermsApprovePathParams(FrozenBaseModel):
    application_id: str = Field()


class FiatApplicationSubmitIdentityDocumentRequestData(FrozenBaseModel):
    class IdentityDocument(FrozenBaseModel):
        cuil: str

    identity_document: IdentityDocument = Field()


class FiatApplicationSubmitIdentityDocumentPathParams(FrozenBaseModel):
    application_id: str = Field()


class FiatApplicationAddBankAccountPathParams(FrozenBaseModel):
    application_id: str = Field()


class FiatApplicationAddBankAccountRequestData(FrozenBaseModel):
    class FiatBankAccount(FrozenBaseModel):
        account_identifier_value: str
        account_identifier_type: str
        account_holder_name: str

    fiat_bank_account: FiatBankAccount = Field()


# USDC Swift
class USDCSwiftStatusShowResponse(RailsResponse):
    class Status(FrozenBaseModel):
        deposit: str
        withdrawal: str

    status: Status


class FiatApplicationsQueryParams(FrozenBaseModel):
    currency: str = Field()


class FiatApplicationsShowResponse(RailsResponse):
    applications: List[Application] = Field()


class USDCBankAccountPathParams(FiatApplicationTermsApprovePathParams):
    pass


class USDCSwiftBankAccountShowResponse(RailsResponse):
    bank_account: BankAccount
    auth_flow: Optional[str]


class USDCSwiftBankAccountCreateRequestData(FrozenBaseModel):
    class InputBankAccount(FrozenBaseModel):
        account_identifier_type: str
        account_identifier_value: str
        bank_account_holder_name: str
        bank_city: Optional[str]
        bank_country: Optional[str]
        bank_identifier_type: Optional[str]
        bank_identifier_value: Optional[str]
        bank_name: Optional[str]

    bank_account: InputBankAccount = Field()


class USDCSwiftBankAccountCreateResponse(RailsResponse):
    application: Application


class USDCSwiftBankAccountCreateAddressRequestData(FrozenBaseModel):
    address: ApplicationAddress


class USDCSwiftBankAccountCreateAddressResponse(RailsResponse):
    application: Application


class USDCSwiftBankAccountActivateRequestData(FiatApplicationsQueryParams):
    pass


class USDCSwiftBankAccountActivateResponse(USDCSwiftBankAccountCreateResponse):
    pass


class USDCSwiftBankAccountProofRequestData(FrozenBaseModel):
    proof_scan_reference: str = Field(default=uuid.uuid4().__str__())


# Send Viban info email
class VibanBankInfoEmailRequestData(FrozenBaseModel):
    currency: str
    viban_type: str
    application_id: Optional[str]


class VibanBankInfoEmail(FrozenBaseModel):
    viban_type: str
    currency: str
    verification_code: str


class VibanBankInfoEmailResponse(RailsResponse):
    bank_info_email: VibanBankInfoEmail


# Crypto_withdrawals
class VibanCryptoWithdrawalBeneficiariesQueryParams(VibanWithdrawalBeneficiariesQueryParams):
    pass


class VibanCryptoWithdrawalBeneficiariesResponse(VibanWithdrawalBeneficiariesResponse):
    pass


class VibanCryptoWithdrawalOrderCreateRequestData(VibanWithdrawalOrdersCreateRequestData):
    pass


class VibanCryptoWithdrawalOrderCreateResponse(RailsResponse):
    order: VibanWithdrawalOrder


class VibanCryptoWithdrawalCreateRequestData(VibanWithdrawalCreateRequestData):
    pass


class VibanCryptoWithdrawalCreateNotOtpRequestData(VibanWithdrawalCreateNoOtpRequestData):
    order_id: str = Field()


class VibanCryptoWithdrawalCreateResponse(VibanWithdrawalCreateResponse):
    pass


class DepositRequestsOverviewQueryParams(FrozenBaseModel):
    currency: str
    payment_network: str


class DepositRequestsOverviewResponse(RailsResponse):
    class OverView(FrozenBaseModel):
        currency: str
        payment_network: str
        minimum_deposit_amount: Balance
        daily_quota: Balance
        used_daily_quota: Balance
        remaining_daily_quota: Balance
        monthly_quota: Balance
        used_monthly_quota: Balance
        remaining_monthly_quota: Balance
        outstanding_amount: Balance
        review_time_description: str
        bank_transfer_time_description: Optional[str]
        status: Optional[str]
        fee: Optional[list]
        bank_accounts_max: Decimal
        transactions_per_day: Decimal
        transactions_per_month: Decimal
        remaining_transactions_daily_count: Decimal
        remaining_transactions_monthly_count: Decimal
        maximum_transaction_amount: Optional[str]

    overview: OverView


class DepositRequestsRequestData(RailsEncryptedPasscodeRequest):
    payment_network: str = Field()
    bank_account_id: str = Field()
    amount: str = Field()
    currency: str = Field()
    biometric: bool = Field(default=False)


class History(FrozenBaseModel):
    timestamp: Optional[str]
    created_at: Optional[str]
    event_type: Optional[str]
    state: Optional[str]


class DepositRequestsResponse(RailsResponse):
    class DepositRequest(FrozenBaseModel):
        class History(FrozenBaseModel):
            class OpeningBalance(FrozenBaseModel):
                current: float
                pending: float
                available: float

            created_at: str
            event_type: str
            opening_balance: OpeningBalance

        class Sender(FrozenBaseModel):
            class Data(FrozenBaseModel):
                bank_account_id: str
                payment_network_identifier_value: str

            id: str
            account_id: str
            vendor_id: str
            sender_identifier: str
            account_identifier_type: str
            account_identifier_value: str
            payment_network_identifier_value: str
            bank_account_id: str
            name: str
            currency: str
            payment_network: str
            data: Data
            is_whitelisted: bool
            created_at: str
            updated_at: str

        class AdditionalInfo(FrozenBaseModel):
            pass

        class BankAccount(FrozenBaseModel):
            class VerificationDetails(FrozenBaseModel):
                class Parent(FrozenBaseModel):
                    id: str
                    type: str

                class Status(FrozenBaseModel):
                    class Validation(FrozenBaseModel):
                        state: str

                    class Verification(FrozenBaseModel):
                        state: str
                        history: List[History]

                    state: str
                    history: List[History]
                    validation: Validation
                    verification: Verification

                class Details(FrozenBaseModel):
                    type: str
                    value: str

                class MetaData(FrozenBaseModel):
                    xyz: str
                    abc123: str

                class FingerPrints(FrozenBaseModel):
                    type: str
                    value: str

                class NamesOnAccount(FrozenBaseModel):
                    name: str
                    type: str

                class CorrelationRefs(FrozenBaseModel):
                    label: str
                    value: str

                id: str
                type: str
                parent: Parent
                status: Status
                country: str
                created: str
                details: Details
                updated: str
                metadata: MetaData
                fingerprints: List[FingerPrints]
                namesOnAccount: List[NamesOnAccount]
                correlationRefs: List[CorrelationRefs]

            id: str
            account_id: str
            status: str
            currency: str
            account_identifier_type: str
            account_identifier_value: str
            payment_network_identifier_value: str
            account_holder_name: str
            verified_by: str
            reason: str
            created_at: str
            updated_at: str
            verification_details: VerificationDetails
            instant_buy_enabled: bool
            supported_payment_networks: List[str]
            user_uuid: str

        class DepositAuthorization(FrozenBaseModel):
            id: str
            deposit_id: str
            status: str
            history: List[History]
            created_at: str
            updated_at: str
            auto_approver_reviewing_status: str

        id: str
        account_id: str
        status: str
        vendor_id: str
        vendor_transaction_type: str
        sender_id: str
        payment_network: str
        currency: str
        amount: str
        fee_currency: str
        fee_amount: str
        history: List[History]
        sender: Sender
        bank_account: BankAccount
        additional_info: Optional[AdditionalInfo]
        created_at: str
        updated_at: str
        deposit_authorization: DepositAuthorization
        identity_name: str
        user_uuid: str
        user_email: str

    deposit_request: DepositRequest = Field()


class BankAccounts(FrozenBaseModel):
    id: str
    account_id: str
    status: str
    currency: str
    bank_name: Optional[str]
    account_identifier_type: str
    account_identifier_value: str
    instant_buy_enabled: bool


class FiatBankAccountsResponse(RailsResponse):
    bank_accounts: List[BankAccounts] = Field()


class FiatDeleteBankAccountResponse(RailsResponse):
    bank_account: BankAccounts = Field()


# Fiat Application
class FiatWalletsApplicationShowQueryParams(FrozenBaseModel):
    vendor_id: str = Optional[str]
    payment_network: str = Optional[str]


class FiatWalletsApplicationResponse(RailsResponse):
    application: Application


# Fiat Wallet Application Countries
class FiatWalletApplicationCountriesResponse(RailsResponse):
    class Counties(FrozenBaseModel):
        translation_key: str
        value: str

    countries: List[Counties]


# Get Fiat Wallet Application Prefill Address
class FiatWalletApplicationPrefillAddressResponse(RailsResponse):
    address: UKFPSSubmitAddressRequestData.Address
    prefill: bool


# Fiat Bank Account Submit Proof
class FiatBankAccountsIdPathParams(FiatDeleteBankAccountsPathParams):
    pass


class FiatBankAccountsSubmitProofRequestData(DcBankApplicationAddressProofRequestData):
    pass


class FiatBankAccountsSubmitProofResponse(FiatDeleteBankAccountResponse):
    pass
