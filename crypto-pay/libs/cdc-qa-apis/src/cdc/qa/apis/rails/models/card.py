import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from . import FrozenBaseModel, RailsResponse, RailsEncryptedPasscodeRequest
from pydantic import Field
from .common import Balance, Quotation, Transaction, TransferUser


# CardShow
class ShowResponse(RailsResponse):
    class Card(FrozenBaseModel):
        id: Optional[int]
        status: str
        holder_name: str
        masked_number: str
        card_type: str
        card_name: str
        currency: str
        activated: bool
        freezed: bool
        international_enabled: bool
        pin_set: bool
        force_freezed: bool
        eu_card: bool
        virtual_card_supported: bool
        physical_card_status: str

    card: Card = Field()


# CardReservationUpdate
class ReservationUpdateRequestData(FrozenBaseModel):
    card_type: str = Field()


class CardReservation(FrozenBaseModel):
    choice: Optional[str]
    locked: Optional[str]
    amount_to_lock: str
    net_amount_to_lock: str
    locked_amount: str
    net_native_amount_to_lock: Balance
    locked_native_amount: Balance
    amount_to_be_locked: Balance
    net_amount_to_be_locked: Balance
    amount_locked: Balance
    native_net_amount_to_be_locked: Balance
    native_amount_locked: Balance
    vip: bool
    lock_until: Optional[datetime]


class ReservationUpdateResponse(RailsResponse):

    card_reservation: CardReservation = Field()


class ReservationShowResponse(ReservationUpdateResponse):
    pass


# FiatAccountShow
class FiatAccountShowResponse(RailsResponse):
    class Account(FrozenBaseModel):
        class Wallet(FrozenBaseModel):
            currency: str
            balance: Balance
            native_balance: Balance

        native_currency: str
        balance: Balance
        native_balance: Balance
        wallets: List[Wallet]

    account: Account = Field()


# FiatExchangeQuotationCreate
class FiatExchangeQuotationCreateRequestData(FrozenBaseModel):
    from_amount: Decimal
    from_side: str = Field(alias="from")
    to: str


class FiatExchangeQuotationCreateResponse(RailsResponse):
    quotation: Quotation


# FiatExchangeCreate
class FiatExchangeCreateRequestData(RailsEncryptedPasscodeRequest):
    quotation_id: str


class Exchange(FrozenBaseModel):
    id: str
    amount: Balance
    to_amount: Balance
    native_amount: Decimal
    rate: Decimal


class FiatExchangeCreateResponse(RailsResponse):

    exchange: Exchange


# --------------------------------- MCO FiatTopUpQuotationCreate --------------------------------- #
class FiatTopUpQuotationCreateRequestData(FrozenBaseModel):
    to_amount: str = Field()
    from_side: str = Field(alias="from")
    to: str = Field()


class FiatTopUpQuotationCreateResponse(RailsResponse):
    quotation: Quotation = Field()


# --------------------------------- MCO FiatTopUpCreate --------------------------------- #
class FiatTopUpCreateRequestData(RailsEncryptedPasscodeRequest):
    quotation_id: str


class FiatTopUpCreateResponse(RailsResponse):
    top_up: Exchange


# --------------------------------- MCO Card Txn --------------------------------- #
class FiatTransactionRequestParams(FrozenBaseModel):
    count: int = Field(default=20)


class FiatTransactionResponse(RailsResponse):
    class Transaction(FrozenBaseModel):
        id: str
        context: str
        nature: str
        description: str
        rate: str
        rate_desc: Optional[str]
        amount: Balance
        to_amount: Optional[Balance]
        native_amount: Optional[Balance]
        status: Optional[str]
        note: Optional[str]
        created_at: str
        updated_at: str
        transaction_type: object
        transfer_meta: object
        meta: object

    transactions: List[Transaction] = Field()


# --------------------------------- AUS MCO Card Accept terms --------------------------------- #
class AusCardAcceptTermsRequestData(FrozenBaseModel):
    version: str


class AusCardAcceptTermsResponse(RailsResponse):
    pass


# --------------------------------- AUS MCO Card Input Residential Address --------------------------------- #
class AusResidentialAddress(FrozenBaseModel):
    town: str
    state: str
    country: str = Field(default="Australia")
    postcode: Optional[str]
    address_1: str
    address_2: str = Field(default="")


class AusResidentialAddressShowResponse(RailsResponse):
    address: AusResidentialAddress
    address_verification: str


class AusResidentialAddressUpdateRequestData(AusResidentialAddress):
    pass


class AusResidentialAddressUpdateResponse(RailsResponse):
    pass


# --------------------------------- AUS MCO Card Address Proof--------------------------------- #
class AusAddressProofRequestData(FrozenBaseModel):
    proof_scan_reference: str = Field(default=uuid.uuid4().__str__())


class AusAddressProofResponse(RailsResponse):
    address_proof: str


# --------------------------------- MCO Card Prefer Name--------------------------------- #
class MCOCardPreferNameRequestData(FrozenBaseModel):
    first_name: str
    last_name: str


class MCOCardPreferNameResponse(RailsResponse):
    pass


# --------------------------------- AUS MCO Card show--------------------------------- #
class AusCardApplicationResponse(RailsResponse):
    class AusCardApplicationProcess(FrozenBaseModel):
        card_type: str
        locked: bool
        application_completed: bool
        address_verification: str
        preferred_name: str
        card_status: Optional[str]
        shipping: Optional[str]
        terms_accepted: bool
        first_name: Optional[str]
        last_name: Optional[str]

    au_card_application: AusCardApplicationProcess


# --------------------------------- Physical application show--------------------------------- #
class PhysicalApplicationShowResponse(RailsResponse):
    class ShipState(FrozenBaseModel):
        state: str
        shipping: Optional[str]

    physical_card_application: ShipState


# --------------------------------- Physical application submit--------------------------------- #
class PhysicalApplicationSubmitResponse(PhysicalApplicationShowResponse):
    pass


# --------------------------------- BRA Physical application show --------------------------------- #
class BraPhysicalApplicationShowResponse(RailsResponse):
    class BraPhysicalApplication(FrozenBaseModel):
        locked: bool
        address_verification: str
        terms_accepted: bool
        shipping_address_submitted: bool
        card_type: Optional[str]
        card_status: Optional[str]
        preferred_name: str
        first_na: Optional[str]
        last_name: Optional[str]
        fiat_terms_accepted: bool
        shipping: Optional[bool]
        application_completed: bool

    br_card_application: BraPhysicalApplication


# --------------------------------- BRA Physical shipping address update --------------------------------- #
class BraAddress(FrozenBaseModel):
    complement: str
    county: str = Field(default="Brasilia")
    neighborhood: str
    state_code: str = Field(default="CE")
    street: str
    street_number: str
    zip_code: str = Field(default="70910900")


class BraPhysicalShippingAddressUpdateRequestData(FrozenBaseModel):
    address: BraAddress


class BraPhysicalShippingAddressUpdateResponse(RailsResponse):
    pass


# MCO Card top up
class VibanCardTopUpCreateOrderRequestData(FrozenBaseModel):
    amount: str
    card_currency: str
    viban_currency: str
    fixed_side: str = Field(default="card")


class VibanCardTopUpCreateOrderResponse(RailsResponse):
    class VibanCardTopUpOrder(FrozenBaseModel):
        id: str
        user_uuid: str
        fixed_side: str = Field(default="card")
        viban_currency: str
        viban_amount: Balance
        card_currency: str
        card_amount: Balance
        fee: Balance
        execute_rate: Optional[str]
        total_charge_amount: Balance
        created_at: str
        updated_at: str

    viban_card_top_up_order: VibanCardTopUpOrder


class VibanCardTopUpsCreateRequestData(RailsEncryptedPasscodeRequest):
    order_id: str
    biometric: bool = Field(default=False)


class VibanCardTopUpsCreateResponse(RailsResponse):
    transaction: Transaction


# MCO cards send to contacts
class McoCardSendToContactsRequestData(RailsEncryptedPasscodeRequest):
    amount: str
    currency: str
    note: Optional[str]
    to_name: str
    to_phone: str
    biometric: bool = Field(default=False)


class McoCardSendToContactsResponse(RailsResponse):
    class McoCardTransfer(FrozenBaseModel):
        id: str
        context: str
        nature: str
        description: str
        rate: str
        from_user: TransferUser
        to_user: TransferUser
        sending: bool
        amount: Balance
        native_amount: Balance
        status: str
        note: Optional[str]
        created_at: str
        updated_at: str

        class TransferType(FrozenBaseModel):
            code: str

            class Description(FrozenBaseModel):
                desc: str
                abbr: str

            description: Description

        class TransferMeta(FrozenBaseModel):
            direction: str
            user_id: int

        transaction_type: TransferType
        transfer_meta: TransferMeta
        meta: Optional[str]

    transfer: McoCardTransfer


# CAD Mco Card - Accept Terms
class CadCardAcceptTermsRequestData(AusCardAcceptTermsRequestData):
    pass


class CadCardAcceptTermsResponse(AusCardAcceptTermsResponse):
    pass


# CAD Mco Card - Application show
class CadCardApplicationShowResponse(RailsResponse):
    class CadApplication(AusCardApplicationResponse.AusCardApplicationProcess):
        fiat_terms_accepted: bool

    ca_card_application: CadApplication


# CAD Mco Card - Dc bank Application state show
class CadDcBankApplicationStateResponse(RailsResponse):
    class Application(FrozenBaseModel):
        class Retry(FrozenBaseModel):
            attempted: int
            remaining_attempts: int

        state: str
        retry: Retry
        resubmit_fields: List[str]

    ca_dcbank_application: Application


# CAD Mco Card - Occupation
class CadDcBankOccupation(FrozenBaseModel):
    key: str
    translation_key: str
    require_specification: bool
    specification: Optional[str]


class CadDcBankOccupationRequestData(FrozenBaseModel):
    occupation: CadDcBankOccupation


class CadDcBankOccupationResponse(RailsResponse):
    pass


class CadDcBankOccupationsSelectedResponse(RailsResponse):
    occupation: Optional[List[CadDcBankOccupation]]


class CadDcBankOccupationsResponse(CadDcBankOccupationsSelectedResponse):
    pass


# CAD Mco Card - Source Funds
class CadDcBankSourceFunds(FrozenBaseModel):
    key: str
    translation_key: str


class CadDcBankSourceFundsSelectedResponse(RailsResponse):
    source_of_funds: Optional[List[CadDcBankSourceFunds]]


class CadDcBankSourceFundsRequestData(FrozenBaseModel):
    source_of_funds: List[str]


class CadDcBankSourceFundsResponse(CadDcBankSourceFundsSelectedResponse):
    pass


# CAD Mco Card - Address
class CadDcBankAddress(FrozenBaseModel):
    id: Optional[str]
    user_id: Optional[int]
    address_1: Optional[str]
    address_2: Optional[str]
    city: Optional[str]
    country: Optional[str]
    postcode: Optional[str]
    proof_scan_reference: Optional[str]
    proof_scan_provider: Optional[str]
    verification: str
    created_at: Optional[str]
    updated_at: Optional[str]
    state_code: Optional[str]
    zip_code: Optional[str]
    province: Optional[str]
    log_data: Optional[str]


class CadDcBankAddressRequestData(FrozenBaseModel):
    class Address(FrozenBaseModel):
        address_1: str
        city: str
        country: str
        zip_code: str
        province: str

    address: Address
    province_key: str


class CadDcBankAddressResponse(RailsResponse):
    address: CadDcBankAddress
    province_key: Optional[str]
    provinces: Optional[List[CadDcBankSourceFunds]]
    address_submission_skippable: bool


class CadDcBankAddressProofRequestData(AusAddressProofRequestData):
    pass


class CadDcBankAddressProofResponse(AusAddressProofResponse):
    pass


# SG MCO Cards - Accept Terms
class SgdCardAcceptTermsRequestData(FrozenBaseModel):
    pass


class SgdCardAcceptTermsResponse(RailsResponse):
    pass


class SgdCardApplicationShowResponse(RailsResponse):
    class SgdCardApplication(AusCardApplicationResponse.AusCardApplicationProcess):
        shipping_address_submitted: bool

    sg_card_application: SgdCardApplication


# EU MCO Cards - Accept Terms
class EuCardAcceptTermsResponse(RailsResponse):
    pass


# EU MCO Cards - Address
class EuCardAddress(FrozenBaseModel):
    class Country(FrozenBaseModel):
        id: int
        name: str
        code: str
        ready_to_ship: bool
        created_at: str
        updated_at: str

    address_1: str
    address_2: str
    city: str
    state: Optional[str]
    postcode: str
    country_code: str
    country: Optional[Country]


class EuCardAddressShowResponse(RailsResponse):
    address: EuCardAddress


class EuCardAddressUpdateRequestData(FrozenBaseModel):
    address: EuCardAddress


class EuCardAddressUpdateResponse(RailsResponse):
    state: str


class EuCardAddressProofRequestData(AusAddressProofRequestData):
    pass


class EuCardAddressProofResponse(AusAddressProofResponse):
    pass


# Card Application Show
class CardApplicationShowResponse(RailsResponse):
    class Application(FrozenBaseModel):
        locked: bool
        address_verification: str
        terms_accepted: bool
        card_status: Optional[str]
        card_type: str
        state: str
        preferred_name: str
        first_name: Optional[str]
        last_name: Optional[str]
        application_completed: bool
        new_tnc_required: bool
        region: Optional[str]

    card_application: Application
