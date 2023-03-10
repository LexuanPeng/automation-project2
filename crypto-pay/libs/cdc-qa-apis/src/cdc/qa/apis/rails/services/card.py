from typing import Union, List

from cdc.qa.apis.rails.services.mco_lockup import PlanId

from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.rails.models import RailsRestApi, RailsRestService
from cdc.qa.apis.rails.models.card import (
    ReservationUpdateRequestData,
    ReservationUpdateResponse,
    ShowResponse,
    FiatAccountShowResponse,
    FiatExchangeQuotationCreateRequestData,
    FiatExchangeQuotationCreateResponse,
    FiatExchangeCreateRequestData,
    FiatExchangeCreateResponse,
    FiatTopUpQuotationCreateRequestData,
    FiatTopUpQuotationCreateResponse,
    FiatTopUpCreateRequestData,
    FiatTopUpCreateResponse,
    FiatTransactionRequestParams,
    FiatTransactionResponse,
    ReservationShowResponse,
    AusCardAcceptTermsRequestData,
    AusCardAcceptTermsResponse,
    AusResidentialAddress,
    AusResidentialAddressUpdateResponse,
    AusResidentialAddressShowResponse,
    AusResidentialAddressUpdateRequestData,
    AusAddressProofRequestData,
    AusAddressProofResponse,
    MCOCardPreferNameRequestData,
    MCOCardPreferNameResponse,
    AusCardApplicationResponse,
    PhysicalApplicationShowResponse,
    BraPhysicalApplicationShowResponse,
    PhysicalApplicationSubmitResponse,
    BraPhysicalShippingAddressUpdateRequestData,
    BraPhysicalShippingAddressUpdateResponse,
    BraAddress,
    VibanCardTopUpCreateOrderRequestData,
    VibanCardTopUpCreateOrderResponse,
    VibanCardTopUpsCreateRequestData,
    VibanCardTopUpsCreateResponse,
    McoCardSendToContactsRequestData,
    McoCardSendToContactsResponse,
    CadCardAcceptTermsRequestData,
    CadCardAcceptTermsResponse,
    CadCardApplicationShowResponse,
    CadDcBankOccupationsSelectedResponse,
    CadDcBankOccupationsResponse,
    CadDcBankOccupationRequestData,
    CadDcBankOccupationResponse,
    CadDcBankSourceFundsSelectedResponse,
    CadDcBankSourceFundsRequestData,
    CadDcBankSourceFundsResponse,
    CadDcBankAddressProofRequestData,
    CadDcBankAddressProofResponse,
    CadDcBankAddressResponse,
    CadDcBankAddressRequestData,
    CadDcBankOccupation,
    CadDcBankApplicationStateResponse,
    SgdCardAcceptTermsRequestData,
    SgdCardAcceptTermsResponse,
    SgdCardApplicationShowResponse,
    EuCardAcceptTermsResponse,
    EuCardAddressShowResponse,
    EuCardAddressUpdateRequestData,
    EuCardAddressUpdateResponse,
    EuCardAddressProofRequestData,
    EuCardAddressProofResponse,
    EuCardAddress,
    CardApplicationShowResponse,
)


class ShowApi(RailsRestApi):
    """Show user's MCO card status"""

    path = "card/show"
    method = HttpMethods.GET
    response_type = ShowResponse


class MCOPreferNameApi(RailsRestApi):
    """MCO card prefer name api"""

    path = "card/prefer_name"
    method = HttpMethods.POST
    request_data_type = MCOCardPreferNameRequestData
    response_type = MCOCardPreferNameResponse


class PhysicalApplicationShowApi(RailsRestApi):
    """Physical Application Show api"""

    path = "card/physical_card_application/show"
    method = HttpMethods.GET
    response_type = PhysicalApplicationShowResponse


class PhysicalApplicationSubmitApi(RailsRestApi):
    """Physical Application submit api"""

    path = "card/physical_card_application/submit"
    method = HttpMethods.POST
    response_type = PhysicalApplicationSubmitResponse


class ReservationShowApi(RailsRestApi):
    """Show reservation for order"""

    path = "card/reservation/show"
    method = HttpMethods.GET
    response_type = ReservationShowResponse


class ReservationUpdateApi(RailsRestApi):
    """Make reservation for cro stake order"""

    path = "card/reservation/update"
    method = HttpMethods.POST
    request_data_type = ReservationUpdateRequestData
    response_type = ReservationUpdateResponse


class FiatAccountShowApi(RailsRestApi):
    """Get balance for each fiat in MCO card"""

    path = "fiat/account/show"
    method = HttpMethods.GET
    response_type = FiatAccountShowResponse


class FiatExchangeQuotationCreateApi(RailsRestApi):
    """Create a quotation for fiat exchange in MCO card"""

    path = "fiat/exchanges/quotation/create"
    method = HttpMethods.POST
    request_data_type = FiatExchangeQuotationCreateRequestData
    response_type = FiatExchangeQuotationCreateResponse


class FiatExchangeCreateApi(RailsRestApi):
    """Create a transaction for fiat exchange in MCO card"""

    path = "fiat/exchanges/create"
    method = HttpMethods.POST
    request_data_type = FiatExchangeCreateRequestData
    response_type = FiatExchangeCreateResponse


class FiatTopUpQuotationCreateApi(RailsRestApi):
    """MCO Fiat top up quotation create in MCO card"""

    path = "fiat/top_ups/quotation/create"
    method = HttpMethods.POST
    request_data_type = FiatTopUpQuotationCreateRequestData
    response_type = FiatTopUpQuotationCreateResponse


class FiatTopUpCreateApi(RailsRestApi):
    """MCO FIat top up create in MCO card"""

    path = "fiat/top_ups/create"
    method = HttpMethods.POST
    request_data_type = FiatTopUpCreateRequestData
    response_type = FiatTopUpCreateResponse


class FiatTransactionApi(RailsRestApi):
    """MCO FIat txn in MCO card"""

    path = "mco_cards/transactions"
    method = HttpMethods.GET
    request_data_type = FiatTransactionRequestParams
    response_type = FiatTransactionResponse


class AusCardAcceptTermsApi(RailsRestApi):
    """Aus card Accept terms"""

    path = "au_card_application/accept_terms"
    method = HttpMethods.POST
    request_data_type = AusCardAcceptTermsRequestData
    response_type = AusCardAcceptTermsResponse


class AusResidentialAddressShowApi(RailsRestApi):
    """Aus card residential address show api"""

    path = "au_card_application/residential_address"
    method = HttpMethods.GET
    response_type = AusResidentialAddress


class AusResidentialAddressUpdateApi(RailsRestApi):
    """Aus card residential address update api"""

    path = "au_card_application/residential_address"
    method = HttpMethods.POST
    request_data_type = AusResidentialAddressUpdateRequestData
    response_type = AusResidentialAddressUpdateResponse


class AusAddressProofApi(RailsRestApi):
    """Aus card address proof api"""

    path = "au_card_application/address_proof"
    method = HttpMethods.POST
    request_data_type = AusAddressProofRequestData
    response_type = AusAddressProofResponse


class AusCardApplicationProcessApi(RailsRestApi):
    """Aus card application process api"""

    path = "au_card_application/show"
    method = HttpMethods.GET
    response_type = AusCardApplicationResponse


class BraPhysicalApplicationShowApi(RailsRestApi):
    """Bra card application show api"""

    path = "br_card_application/show"
    method = HttpMethods.GET
    response_type = BraPhysicalApplicationShowResponse


class BraPhysicalShippingAddressUpdateApi(RailsRestApi):
    """Bra Physical Shipping Address Update Api"""

    path = "br_card_application/shipping_address/update"
    method = HttpMethods.POST
    request_data_type = BraPhysicalShippingAddressUpdateRequestData
    response_type = BraPhysicalShippingAddressUpdateResponse


class VibanCardTopUpCreateOrderApi(RailsRestApi):
    """Mco card top up create order api"""

    path = "viban/card_top_up/orders/create"
    method = HttpMethods.POST
    request_data_type = VibanCardTopUpCreateOrderRequestData
    response_type = VibanCardTopUpCreateOrderResponse


class VibanCardTopUpsCreateApi(RailsRestApi):
    """Mco card top up create api"""

    path = "viban/card_top_ups/create"
    method = HttpMethods.POST
    request_data_type = VibanCardTopUpsCreateRequestData
    response_type = VibanCardTopUpsCreateResponse


class McoCardSendToContactsApi(RailsRestApi):
    """Mco card send to contact api"""

    path = "mco_cards/transfers/create"
    method = HttpMethods.POST
    request_data_type = McoCardSendToContactsRequestData
    response_type = McoCardSendToContactsResponse


class CadCardAcceptTermsApi(RailsRestApi):
    """CAD Mco Card - Accept Terms api"""

    path = "ca_card_application/accept_terms"
    method = HttpMethods.POST
    request_data_type = CadCardAcceptTermsRequestData
    response_type = CadCardAcceptTermsResponse


class CadDcBankApplicationStateApi(RailsRestApi):
    """CAD Mco Card - dc bank application state show api"""

    path = "ca_dcbank_application"
    method = HttpMethods.GET
    response_type = CadDcBankApplicationStateResponse


class CadDcBankApplicationTriggerApi(RailsRestApi):
    """CAD Mco Card - dc bank application state show api"""

    path = "ca_dcbank_application"
    method = HttpMethods.POST
    response_type = CadDcBankApplicationStateResponse


class CadCardApplicationShowApi(RailsRestApi):
    """CAD Mco Card - application show api"""

    path = "ca_card_application/show"
    method = HttpMethods.GET
    response_type = CadCardApplicationShowResponse


class CadDcBankOccupationsSelectedApi(RailsRestApi):
    """CAD Mco Card - Occupations selected show"""

    path = "ca_dcbank_application/occupations/selected"
    method = HttpMethods.GET
    response_type = CadDcBankOccupationsSelectedResponse


class CadDcBankOccupationApi(RailsRestApi):
    """CAD Mco Card - update Occupation"""

    path = "ca_dcbank_application/occupation"
    method = HttpMethods.POST
    request_data_type = CadDcBankOccupationRequestData
    response_type = CadDcBankOccupationResponse


class CadDcBankOccupationsApi(RailsRestApi):
    """CAD Mco Card - Occupations show"""

    path = "ca_dcbank_application/occupations"
    method = HttpMethods.GET
    response_type = CadDcBankOccupationsResponse


class CadDcBankSourceFundsSelectedApi(RailsRestApi):
    """CAD Mco Card - Source Funds selected"""

    path = "ca_dcbank_application/source_of_funds/selected"
    method = HttpMethods.GET
    response_type = CadDcBankSourceFundsSelectedResponse


class CadDcBankSourceFundsShowApi(RailsRestApi):
    """CAD Mco Card - Source Funds show"""

    path = "ca_dcbank_application/source_of_funds"
    method = HttpMethods.GET
    response_type = CadDcBankSourceFundsResponse


class CadDcBankSourceFundsApi(RailsRestApi):
    """CAD Mco Card - Source Funds update"""

    path = "ca_dcbank_application/source_of_funds"
    method = HttpMethods.POST
    request_data_type = CadDcBankSourceFundsRequestData
    response_type = CadDcBankSourceFundsResponse


class CadDcBankAddressShowApi(RailsRestApi):
    """CAD Mco Card - Address show"""

    path = "ca_dcbank_application/address"
    method = HttpMethods.GET
    response_type = CadDcBankAddressResponse


class CadDcBankAddressApi(RailsRestApi):
    """CAD Mco Card - Address update"""

    path = "ca_dcbank_application/address"
    method = HttpMethods.POST
    request_data_type = CadDcBankAddressRequestData
    response_type = CadDcBankAddressResponse


class CadDcBankAddressProofApi(RailsRestApi):
    """CAD Mco Card - Source Funds address proof"""

    path = "ca_dcbank_application/address_proof"
    method = HttpMethods.POST
    request_data_type = CadDcBankAddressProofRequestData
    response_type = CadDcBankAddressProofResponse


class SgdCardAcceptTermsApi(RailsRestApi):
    """SGD Mco Card - Accept Terms api"""

    path = "sg_card_application/accept_terms"
    method = HttpMethods.POST
    request_data_type = SgdCardAcceptTermsRequestData
    response_type = SgdCardAcceptTermsResponse


class SgdCardApplicationShowApi(RailsRestApi):
    """SGD Mco Card - Application show api"""

    path = "sg_card_application/show"
    method = HttpMethods.GET
    response_type = SgdCardApplicationShowResponse


class EuCardAcceptTermsApi(RailsRestApi):
    """EuCardAcceptTermsApi"""

    path = "eu_card_application/confirm_tnc"
    method = HttpMethods.POST
    response_type = EuCardAcceptTermsResponse


class EuCardAddressShowApi(RailsRestApi):
    """EuCardAddressShowApi"""

    path = "eu_card_application/address/show"
    method = HttpMethods.GET
    response_type = EuCardAddressShowResponse


class EuCardAddressUpdateApi(RailsRestApi):
    """EU Mco Card - address update api"""

    path = "eu_card_application/update"
    method = HttpMethods.POST
    request_data_type = EuCardAddressUpdateRequestData
    response_type = EuCardAddressUpdateResponse


class EuCardAddressProofApi(RailsRestApi):
    """EU Mco Card - address update proof api"""

    path = "eu_card_application/address_proof/update"
    method = HttpMethods.POST
    request_data_type = EuCardAddressProofRequestData
    response_type = EuCardAddressProofResponse


class CardApplicationShowApi(RailsRestApi):
    """CardApplication- address show api"""

    path = "card/application/show"
    method = HttpMethods.GET
    response_type = CardApplicationShowResponse


class CardService(RailsRestService):
    def show(self) -> ShowResponse:
        api = ShowApi(host=self.host, _session=self.session)

        response = api.call()
        return ShowResponse.parse_raw(b=response.content)

    def reservation_update(self, card_tier: str) -> ReservationUpdateResponse:
        api = ReservationUpdateApi(host=self.host, _session=self.session)
        data = ReservationUpdateRequestData(card_type=card_tier).dict(exclude_none=True)

        response = api.call(data=data)
        return ReservationUpdateResponse.parse_raw(b=response.content)

    def fiat_account_show(self) -> FiatAccountShowResponse:
        api = FiatAccountShowApi(host=self.host, _session=self.session)

        response = api.call()
        return FiatAccountShowResponse.parse_raw(b=response.content)

    def _fiat_exchange_quotation_create(
        self, from_amount: str, from_currency: str, to_currency: str
    ) -> FiatExchangeQuotationCreateResponse:
        api = FiatExchangeQuotationCreateApi(host=self.host, _session=self.session)
        params = {
            "from_amount": from_amount,
            "from": from_currency,
            "to": to_currency,
        }
        data = FiatExchangeQuotationCreateRequestData(**params).dict(exclude_none=True, by_alias=True)

        response = api.call(data=data)
        return FiatExchangeQuotationCreateResponse.parse_raw(b=response.content)

    def _fiat_exchange_create(self, passcode: str, quotation_id: str) -> FiatExchangeCreateResponse:
        api = FiatExchangeCreateApi(host=self.host, _session=self.session)
        data = FiatExchangeCreateRequestData(passcode=passcode, quotation_id=quotation_id).dict(exclude_none=True)

        response = api.call(data=data)
        return FiatExchangeCreateResponse.parse_raw(b=response.content)

    def fiat_exchange(self, passcode: Union[str, int], from_amount: str, from_currency: str, to_currency: str):
        quotation_id = self._fiat_exchange_quotation_create(
            from_amount=from_amount,
            from_currency=from_currency,
            to_currency=to_currency,
        ).quotation.id
        self._fiat_exchange_create(passcode=str(passcode), quotation_id=quotation_id)

    def top_up_quotation_create(
        self,
        to_amount: str,
        from_side: str,
        to: str,
        side: str = "to_amount",
    ) -> FiatTopUpQuotationCreateResponse:
        api = FiatTopUpQuotationCreateApi(host=self.host, _session=self.session)
        # side: to_amount or from_amount
        params = {
            side: to_amount,
            "from": from_side,
            "to": to,
        }
        data = FiatTopUpQuotationCreateRequestData(**params).dict(exclude_none=True, by_alias=True)

        response = api.call(data=data)
        return FiatTopUpQuotationCreateResponse.parse_raw(b=response.content)

    def top_up_create(self, passcode: Union[str, int], quotation_id: str) -> FiatTopUpCreateResponse:
        api = FiatTopUpCreateApi(host=self.host, _session=self.session)
        data = FiatTopUpCreateRequestData(passcode=passcode, quotation_id=quotation_id).dict(exclude_none=True)

        response = api.call(data=data)
        return FiatTopUpCreateResponse.parse_raw(b=response.content)

    def get_txn(self, count: Union[str, int] = "20") -> FiatTransactionResponse:
        api = FiatTransactionApi(host=self.host, _session=self.session)
        params = FiatTransactionRequestParams(count=str(count)).dict(exclude_none=True)

        response = api.call(params=params)
        return FiatTransactionResponse.parse_raw(b=response.content)

    def reservation_show(self) -> ReservationShowResponse:
        api = ReservationShowApi(host=self.host, _session=self.session)

        response = api.call()
        return ReservationShowResponse.parse_raw(b=response.content)

    def aus_card_accept_terms(self, mco_card_tier: str) -> AusCardAcceptTermsResponse:
        plan_id = PlanId[mco_card_tier].value
        api = AusCardAcceptTermsApi(host=self.host, _session=self.session)
        data = AusCardAcceptTermsRequestData(version=plan_id).dict(exclude_none=True)

        response = api.call(data=data)
        return AusCardAcceptTermsResponse.parse_raw(b=response.content)

    def aus_card_residential_address_show(self) -> AusResidentialAddressShowResponse:
        api = AusResidentialAddressShowApi(host=self.host, _session=self.session)

        response = api.call()
        return AusResidentialAddressShowResponse.parse_raw(b=response.content)

    def aus_card_residential_address_update(
        self, town: str, state: str, country: str, postcode: str, address_1: str, address_2: str = ""
    ) -> AusResidentialAddressUpdateResponse:
        api = AusResidentialAddressUpdateApi(host=self.host, _session=self.session)
        data = AusResidentialAddressUpdateRequestData(
            town=town,
            state=state,
            country=country,
            postcode=postcode,
            address_1=address_1,
            address_2=address_2,
        ).dict(exclude_none=True)

        response = api.call(json=data)
        return AusResidentialAddressUpdateResponse.parse_raw(b=response.content)

    def aus_card_proof(self, proof_scan_reference_id: str = None) -> AusAddressProofResponse:
        api = AusAddressProofApi(host=self.host, _session=self.session)
        if proof_scan_reference_id:
            data = AusAddressProofRequestData(proof_scan_reference=proof_scan_reference_id).dict(exclude_none=True)
        else:
            data = AusAddressProofRequestData().dict(exclude_none=True)

        response = api.call(json=data)
        return AusAddressProofResponse.parse_raw(b=response.content)

    def aus_card_process(self) -> AusCardApplicationResponse:
        api = AusCardApplicationProcessApi(host=self.host, _session=self.session)

        response = api.call()
        return AusCardApplicationResponse.parse_raw(b=response.content)

    def mco_card_prefer_name(self, first_name: str, last_name: str) -> MCOCardPreferNameResponse:
        api = MCOPreferNameApi(host=self.host, _session=self.session)
        data = MCOCardPreferNameRequestData(first_name=first_name, last_name=last_name).dict(exclude_none=True)

        response = api.call(json=data)
        return MCOCardPreferNameResponse.parse_raw(b=response.content)

    def physical_application_show(self) -> PhysicalApplicationShowResponse:
        api = PhysicalApplicationShowApi(host=self.host, _session=self.session)

        response = api.call()
        return PhysicalApplicationShowResponse.parse_raw(b=response.content)

    def physical_application_submit(self) -> PhysicalApplicationSubmitResponse:
        api = PhysicalApplicationSubmitApi(host=self.host, _session=self.session)

        response = api.call()
        return PhysicalApplicationSubmitResponse.parse_raw(b=response.content)

    def bra_physical_application_show(self) -> BraPhysicalApplicationShowResponse:
        api = BraPhysicalApplicationShowApi(host=self.host, _session=self.session)

        response = api.call()
        return BraPhysicalApplicationShowResponse.parse_raw(b=response.content)

    def bra_physical_card_shipping_address_update(
        self, street, street_number, zip_code, county, neighborhood, state_code, complement
    ) -> BraPhysicalShippingAddressUpdateResponse:
        api = BraPhysicalShippingAddressUpdateApi(host=self.host, _session=self.session)
        bra_address = BraAddress(
            complement=complement,
            county=county,
            neighborhood=neighborhood,
            state_code=state_code,
            street=street,
            street_number=street_number,
            zip_code=zip_code,
        )
        data = BraPhysicalShippingAddressUpdateRequestData(address=bra_address).dict(exclude_none=True)

        response = api.call(json=data)
        return BraPhysicalShippingAddressUpdateResponse.parse_raw(b=response.content)

    def viban_card_top_up_create_order(
        self,
        amount: str,
        card_currency: str,
        viban_currency: str,
        fixed_side: str = "card",
    ) -> VibanCardTopUpCreateOrderResponse:
        api = VibanCardTopUpCreateOrderApi(host=self.host, _session=self.session)
        data = VibanCardTopUpCreateOrderRequestData(
            amount=amount,
            card_currency=card_currency,
            viban_currency=viban_currency,
            fixed_side=fixed_side,
        ).dict(exclude_none=True)

        response = api.call(json=data)
        return VibanCardTopUpCreateOrderResponse.parse_raw(b=response.content)

    def viban_card_top_up_create(self, order_id: str, passcode: str) -> VibanCardTopUpsCreateResponse:
        api = VibanCardTopUpsCreateApi(host=self.host, _session=self.session)
        data = VibanCardTopUpsCreateRequestData(order_id=order_id, passcode=passcode).dict(exclude_none=True)

        response = api.call(data=data)
        return VibanCardTopUpsCreateResponse.parse_raw(b=response.content)

    def send_to_contact(
        self,
        amount: str,
        currency: str,
        to_name: str,
        to_phone: str,
        passcode: str,
        note: str = "Auto Test",
    ) -> McoCardSendToContactsResponse:
        api = McoCardSendToContactsApi(host=self.host, _session=self.session)
        data = McoCardSendToContactsRequestData(
            amount=amount,
            currency=currency,
            to_name=to_name,
            to_phone=to_phone,
            note=note,
            passcode=passcode,
        ).dict(exclude_none=True)

        response = api.call(data=data)
        return McoCardSendToContactsResponse.parse_raw(b=response.content)

    def cad_card_accept_terms(self, mco_card_tier: str) -> CadCardAcceptTermsResponse:
        plan_id = PlanId[mco_card_tier].value
        api = CadCardAcceptTermsApi(host=self.host, _session=self.session)
        data = CadCardAcceptTermsRequestData(version=plan_id).dict(exclude_none=True)

        response = api.call(data=data)
        return CadCardAcceptTermsResponse.parse_raw(b=response.content)

    def cad_card_show(self) -> CadCardApplicationShowResponse:
        api = CadCardApplicationShowApi(host=self.host, _session=self.session)
        response = api.call()
        return CadCardApplicationShowResponse.parse_raw(b=response.content)

    def cad_occupations_selected(self) -> CadDcBankOccupationsSelectedResponse:
        api = CadDcBankOccupationsSelectedApi(host=self.host, _session=self.session)
        response = api.call()
        return CadDcBankOccupationsSelectedResponse.parse_raw(b=response.content)

    def cad_occupation_update(
        self,
        require_specification: bool,
        key: str,
        specification: str = "",
        translation_key: str = "cad_fiat_identity_verification_occupation_list_selected__label_",
    ) -> CadDcBankOccupationResponse:
        api = CadDcBankOccupationApi(host=self.host, _session=self.session)
        occupation = CadDcBankOccupation(
            require_specification=require_specification,
            key=key,
            specification=specification,
            translation_key=f"{translation_key}{key.replace('_', '')}",
        )
        data = CadDcBankOccupationRequestData(occupation=occupation).dict(exclude_none=True)

        response = api.call(json=data)
        return CadDcBankOccupationResponse.parse_raw(b=response.content)

    def cad_occupations_show(self) -> CadDcBankOccupationsResponse:
        api = CadDcBankOccupationsApi(host=self.host, _session=self.session)

        response = api.call()
        return CadDcBankOccupationsResponse.parse_raw(b=response.content)

    def cad_source_funds_selected(self) -> CadDcBankSourceFundsSelectedResponse:
        api = CadDcBankSourceFundsSelectedApi(host=self.host, _session=self.session)
        response = api.call()
        return CadDcBankSourceFundsSelectedResponse.parse_raw(b=response.content)

    def cad_source_funds_show(self) -> CadDcBankSourceFundsResponse:
        api = CadDcBankSourceFundsShowApi(host=self.host, _session=self.session)
        response = api.call()
        return CadDcBankSourceFundsResponse.parse_raw(b=response.content)

    def cad_source_funds_update(self, source_of_funds: List[str]) -> CadDcBankSourceFundsResponse:
        api = CadDcBankSourceFundsApi(host=self.host, _session=self.session)
        data = CadDcBankSourceFundsRequestData(source_of_funds=source_of_funds).dict(exclude_none=True)

        response = api.call(json=data)
        return CadDcBankSourceFundsResponse.parse_raw(b=response.content)

    def cad_dc_bank_address_show(self) -> CadDcBankAddressResponse:
        api = CadDcBankAddressShowApi(host=self.host, _session=self.session)
        response = api.call()
        return CadDcBankAddressResponse.parse_raw(b=response.content)

    def cad_dc_bank_address_update(
        self,
        address_1,
        city,
        country,
        zip_code,
        province,
        province_key,
    ) -> CadDcBankAddressResponse:
        api = CadDcBankAddressApi(host=self.host, _session=self.session)
        address = CadDcBankAddressRequestData.Address(
            address_1=address_1,
            city=city,
            country=country,
            zip_code=zip_code,
            province=province,
        )
        data = CadDcBankAddressRequestData(address=address, province_key=province_key).dict(exclude_none=True)

        response = api.call(json=data)
        return CadDcBankAddressResponse.parse_raw(b=response.content)

    def cad_dc_bank_address_proof(self) -> CadDcBankAddressProofResponse:
        api = CadDcBankAddressProofApi(host=self.host, _session=self.session)
        data = CadDcBankAddressProofRequestData().dict(exclude_none=True)

        response = api.call(json=data)
        return CadDcBankAddressProofResponse.parse_raw(b=response.content)

    def cad_dc_bank_state_show(self, action: str = "show") -> CadDcBankApplicationStateResponse:
        if action == "show":
            api = CadDcBankApplicationStateApi(host=self.host, _session=self.session)
        else:
            # To trigger the cad dc bank app and show the address proof
            api = CadDcBankApplicationTriggerApi(host=self.host, _session=self.session)

        response = api.call()
        return CadDcBankApplicationStateResponse.parse_raw(b=response.content)

    def sgd_card_accept_terms(self) -> SgdCardAcceptTermsResponse:
        api = SgdCardAcceptTermsApi(host=self.host, _session=self.session)

        response = api.call()
        return SgdCardAcceptTermsResponse.parse_raw(b=response.content)

    def sgd_card_application_show(self) -> SgdCardApplicationShowResponse:
        api = SgdCardApplicationShowApi(host=self.host, _session=self.session)

        response = api.call()
        return SgdCardApplicationShowResponse.parse_raw(b=response.content)

    def eu_card_accept_terms(self) -> EuCardAcceptTermsResponse:
        api = EuCardAcceptTermsApi(host=self.host, _session=self.session)

        response = api.call()
        return EuCardAcceptTermsResponse.parse_raw(b=response.content)

    def eu_card_address_show(self) -> EuCardAddressShowResponse:
        api = EuCardAddressShowApi(host=self.host, _session=self.session)

        response = api.call()
        return EuCardAddressShowResponse.parse_raw(b=response.content)

    def eu_card_address_update(
        self,
        address_1: str,
        address_2: str,
        city: str,
        country_code: str,
        postcode: str,
    ) -> EuCardAddressUpdateResponse:
        api = EuCardAddressUpdateApi(host=self.host, _session=self.session)
        address = EuCardAddress(
            address_1=address_1,
            address_2=address_2,
            city=city,
            country_code=country_code,
            postcode=postcode,
        )
        data = EuCardAddressUpdateRequestData(address=address).dict(exclude_none=True)

        response = api.call(json=data)
        return EuCardAddressUpdateResponse.parse_raw(b=response.content)

    def eu_card_address_proof(self) -> EuCardAddressProofResponse:
        api = EuCardAddressProofApi(host=self.host, _session=self.session)
        data = EuCardAddressProofRequestData().dict(exclude_none=True)

        response = api.call(json=data)
        return EuCardAddressProofResponse.parse_raw(b=response.content)

    def card_application_show(self) -> CardApplicationShowResponse:
        api = CardApplicationShowApi(host=self.host, _session=self.session)

        response = api.call()
        return CardApplicationShowResponse.parse_raw(b=response.content)
