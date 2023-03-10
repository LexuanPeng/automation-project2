from decimal import Decimal
from typing import List, Optional, Union

from cpf_generator import CPF
from retry import retry
from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.rails.data.fiat import FiatWalletInfo, Fiat
from cdc.qa.apis.rails.models import RailsRestApi, RailsRestService, RailsResponseError
from cdc.qa.apis.rails.models.common import Address
from cdc.qa.apis.rails.models.fiat import (
    CryptoFiatDepositMethodsTermsAcceptRequestData,
    CryptoFiatDepositMethodsTermsAcceptResponse,
    USVanApplicationAddressUpdateRequestData,
    USVanApplicationAddressUpdateResponse,
    USVanApplicationUpdateRequestData,
    USVanApplicationUpdateResponse,
    ACHWithdrawalBankAccountsCreateRequestData,
    ACHWithdrawalBankAccountsCreateResponse,
    XfersTNCCreateRequestData,
    XfersTNCCreateResponse,
    XfersConnectResponse,
    XfersConnectRequestData,
    CryptoFiatDepositMethodsCreateRequestData,
    CryptoFiatDepositMethodsCreateResponse,
    VibanPurchasesQuotationCreateRequestData,
    VibanPurchasesQuotationCreateResponse,
    VibanPurchasesCreateRequestData,
    VibanPurchasesCreateResponse,
    FiatWalletsTransactionsQueryParams,
    FiatWalletsTransactionsResponse,
    XfersPurchaseQuotationCreateRequestData,
    XfersPurchaseQuotationCreateResponse,
    XfersPurchaseCreateRequestData,
    XfersPurchaseCreateResponse,
    XfersSellQuotationCreateRequestData,
    XfersSellQuotationCreateResponse,
    XfersSellCreateRequestData,
    XfersSellCreateResponse,
    ACHWithdrawalWithdrawalCreateRequestData,
    ACHWithdrawalWithdrawalCreateResponse,
    ACHWithdrawalWithdrawalVerifyPasscodeRequestData,
    ACHWithdrawalWithdrawalVerifyPasscodeResponse,
    ACHWithdrawalBankAccountsResponse,
    VibanWithdrawalBeneficiariesQueryParams,
    VibanWithdrawalBeneficiariesResponse,
    VibanWithdrawalOrdersCreateRequestData,
    VibanWithdrawalOrdersCreateResponse,
    VibanWithdrawalCreateRequestData,
    VibanWithdrawalCreateResponse,
    VibanSellQuotationCreateRequestData,
    VibanSellQuotationCreateResponse,
    VibanSellCreateRequestData,
    VibanSellCreateResponse,
    PostVibanWithdrawalBeneficiariesRequestData,
    PostVibanWithdrawalBeneficiariesResponse,
    ExchangesQuotationCreateRequest,
    ExchangesQuotationCreateResponse,
    VibanAccountSummaryResponse,
    XfersAccountShowResponse,
    DcBankGetOccupationResponse,
    DcBankGetSourceOfFundsResponse,
    DcBankSelectOccupationRequestData,
    DcBankSelectOccupationResponse,
    DcBankSelectSourceOfFundsRequestData,
    DcBankSelectSourceOfFundsResponse,
    DcBankSubmitAddressRequestData,
    DcBankSubmitAddressResponse,
    DcBankGetAddressResponse,
    DcBankSubmitApplicationResponse,
    UKFPSSubmitAddressRequestData,
    UKFPSSubmitAddressResponse,
    VibanTermsAcceptRequestData,
    VibanTermsAcceptResponse,
    CryptoFiatDepositMethodsShowPathParams,
    CryptoFiatDepositMethodsShowQueryParams,
    CryptoFiatDepositMethodsShowResponse,
    CADFiatDepositByReferenceNumberOverviewResponse,
    CADFiatDepositCreateRequestData,
    CADFiatDepositCreateResponse,
    BancoPluralApplicationResponse,
    BancoPluralApplicationAddressResponse,
    BancoPluralApplicationCPFResponse,
    BancoPluralApplicationCPFData,
    BancoPluralApplicationAddressData,
    FiatApplicationRequestData,
    FiatApplicationResponse,
    FiatApplicationTermsApprovePathParams,
    VibanWithdrawalCreateNoOtpRequestData,
    USDCSwiftStatusShowResponse,
    FiatApplicationsQueryParams,
    FiatApplicationSubmitIdentityDocumentPathParams,
    FiatApplicationSubmitIdentityDocumentRequestData,
    FiatApplicationAddBankAccountPathParams,
    FiatApplicationAddBankAccountRequestData,
    FiatApplicationsShowResponse,
    USDCBankAccountPathParams,
    USDCSwiftBankAccountShowResponse,
    USDCSwiftBankAccountCreateResponse,
    USDCSwiftBankAccountCreateRequestData,
    USDCSwiftBankAccountCreateAddressRequestData,
    USDCSwiftBankAccountCreateAddressResponse,
    USDCSwiftBankAccountActivateRequestData,
    USDCSwiftBankAccountActivateResponse,
    ApplicationAddress,
    USDCSwiftBankAccountProofRequestData,
    VibanBankInfoEmailRequestData,
    VibanBankInfoEmailResponse,
    VibanCryptoWithdrawalBeneficiariesResponse,
    VibanCryptoWithdrawalBeneficiariesQueryParams,
    VibanCryptoWithdrawalOrderCreateRequestData,
    VibanCryptoWithdrawalOrderCreateResponse,
    VibanCryptoWithdrawalCreateResponse,
    VibanCryptoWithdrawalCreateNotOtpRequestData,
    VibanCryptoWithdrawalCreateRequestData,
    DepositRequestsOverviewQueryParams,
    DepositRequestsOverviewResponse,
    DepositRequestsRequestData,
    DepositRequestsResponse,
    FiatBankAccountsResponse,
    FiatBankAccountsPathParams,
    FiatDeleteBankAccountsPathParams,
    FiatDeleteBankAccountResponse,
    FiatWalletsApplicationShowQueryParams,
    FiatWalletsApplicationResponse,
    UKFPSSubmitAddressProofRequestData,
    UKFPSSubmitAddressProofResponse,
    DcBankApplicationAddressProofRequestData,
    DcBankApplicationAddressProofResponse,
    FiatWalletApplicationCountriesResponse,
    FiatWalletApplicationPrefillAddressResponse,
    FiatBankAccountsIdPathParams,
    FiatBankAccountsSubmitProofRequestData,
    FiatBankAccountsSubmitProofResponse,
)


class CryptoFiatDepositMethodsTermsAcceptApi(RailsRestApi):
    """Accept T&C when user starts to create fiat wallet."""

    path = "v1/crypto_fiat/deposit_methods/terms/accept"
    method = HttpMethods.POST
    request_data_type = CryptoFiatDepositMethodsTermsAcceptRequestData
    response_type = CryptoFiatDepositMethodsTermsAcceptResponse


class USVanApplicationAddressUpdateApi(RailsRestApi):
    """Update user address for US Van Application."""

    path = "us_van_application/address/update"
    method = HttpMethods.POST
    request_data_type = USVanApplicationAddressUpdateRequestData
    response_type = USVanApplicationAddressUpdateResponse


class USVanApplicationUpdateApi(RailsRestApi):
    """Update user Social Security Number."""

    path = "us_van_application/update"
    method = HttpMethods.POST
    request_data_type = USVanApplicationUpdateRequestData
    response_type = USVanApplicationUpdateResponse


class ACHWithdrawalBankAccountsCreateApi(RailsRestApi):
    """Add ACH withdrawal bank account to user account."""

    path = "ach_withdrawal/bank_accounts/create"
    method = HttpMethods.POST
    request_data_type = ACHWithdrawalBankAccountsCreateRequestData
    response_type = ACHWithdrawalBankAccountsCreateResponse


class ACHWithdrawalBankAccountsApi(RailsRestApi):
    path = "ach_withdrawal/bank_accounts"
    method = HttpMethods.GET
    response_type = ACHWithdrawalBankAccountsResponse


class ACHWithdrawalWithdrawalCreateApi(RailsRestApi):
    path = "ach_withdrawal/withdrawal/create"
    method = HttpMethods.POST
    request_data_type = ACHWithdrawalWithdrawalCreateRequestData
    response_type = ACHWithdrawalWithdrawalCreateResponse


class ACHWithdrawalWithdrawalVerifyPasscodeApi(RailsRestApi):
    path = "ach_withdrawal/withdrawal/create/verify_passcode"
    method = HttpMethods.POST
    request_data_type = ACHWithdrawalWithdrawalVerifyPasscodeRequestData
    response_type = ACHWithdrawalWithdrawalVerifyPasscodeResponse


class XfersTNCCreateApi(RailsRestApi):
    """Accept Xfers Terms and Conditions."""

    path = "xfers/tnc/create"
    method = HttpMethods.POST
    request_data_type = XfersTNCCreateRequestData
    response_type = XfersTNCCreateResponse


class XfersConnectApi(RailsRestApi):
    """Conncet Xfers to user account."""

    path = "xfers/connect"
    method = HttpMethods.POST
    request_data_type = XfersConnectRequestData
    response_type = XfersConnectResponse


class CryptoFiatDepositMethodsCreateApi(RailsRestApi):
    """Create fiat deposit methods. Used by SEPA only for now."""

    path = "v1/crypto_fiat/deposit_methods/create"
    method = HttpMethods.POST
    request_data_type = CryptoFiatDepositMethodsCreateRequestData
    response_type = CryptoFiatDepositMethodsCreateResponse


class CryptoFiatDepositMethodsShowApi(RailsRestApi):
    """Show fiat deposit methods. Used by FPS & SG Fast only for now."""

    def path(self, path_params: CryptoFiatDepositMethodsShowPathParams):
        return f"v1/crypto_fiat/deposit_methods/show?currency={path_params.currency}"

    method = HttpMethods.GET
    response_type = CryptoFiatDepositMethodsShowResponse


class VibanAccountSummaryApi(RailsRestApi):
    """Show viban account summary"""

    path = "viban/account/summary"
    method = HttpMethods.GET
    response_type = VibanAccountSummaryResponse


class VibanTermsAcceptApi(RailsRestApi):
    """Accept viban terms"""

    path = "viban/terms/accept"
    method = HttpMethods.POST
    request_data_type = VibanTermsAcceptRequestData
    response_type = VibanTermsAcceptResponse


class VibanPurchasesQuotationCreateApi(RailsRestApi):
    """Create viban purchase quotation."""

    path = "viban/purchases/quotation/create"
    method = HttpMethods.POST
    request_data_type = VibanPurchasesQuotationCreateRequestData
    response_type = VibanPurchasesQuotationCreateResponse


class VibanPurchasesCreateApi(RailsRestApi):
    """Create viban purchase transaction."""

    path = "viban/purchases/create"
    method = HttpMethods.POST
    request_data_type = VibanPurchasesCreateRequestData
    response_type = VibanPurchasesCreateResponse


class VibanSellQuotationCreateApi(RailsRestApi):
    path = "crypto_vibans/quotation/create"
    method = HttpMethods.POST
    request_data_type = VibanSellQuotationCreateRequestData
    response_type = VibanSellQuotationCreateResponse


class VibanSellCreateApi(RailsRestApi):
    path = "crypto_vibans/create"
    method = HttpMethods.POST
    request_data_type = VibanSellCreateRequestData
    response_type = VibanSellCreateResponse


class VibanWithdrawalBeneficiariesApi(RailsRestApi):
    path = "viban/withdrawal_beneficiaries"
    method = HttpMethods.GET
    request_params_type = VibanWithdrawalBeneficiariesQueryParams
    response_type = VibanWithdrawalBeneficiariesResponse


class PostVibanWithdrawalBeneficiariesApi(RailsRestApi):
    path = "viban/withdrawal_beneficiaries"
    method = HttpMethods.POST
    request_params_type = PostVibanWithdrawalBeneficiariesRequestData
    response_type = PostVibanWithdrawalBeneficiariesResponse


class VibanWithdrawalOrdersCreateApi(RailsRestApi):
    path = "viban/withdrawal/orders/create"
    method = HttpMethods.POST
    request_data_type = VibanWithdrawalOrdersCreateRequestData
    response_type = VibanWithdrawalOrdersCreateResponse


class VibanWithdrawalCreateApi(RailsRestApi):
    path = "viban/withdrawals/create"
    method = HttpMethods.POST
    request_data_type = VibanWithdrawalCreateRequestData
    response_type = VibanWithdrawalCreateResponse


class XfersAccountShowApi(RailsRestApi):
    path = "xfers/account/show"
    method = HttpMethods.GET
    response_type = XfersAccountShowResponse


class XfersPurchaseQuotationCreateApi(RailsRestApi):
    """Create xfers purchase quotation."""

    path = "xfers/purchase/quotation/create"
    method = HttpMethods.POST
    request_data_type = XfersPurchaseCreateRequestData
    response_type = XfersPurchaseQuotationCreateResponse


class XfersPurchaseCreateApi(RailsRestApi):
    """Create xfers purchase transaction."""

    path = "xfers/purchase/create"
    method = HttpMethods.POST
    request_data_type = XfersPurchaseCreateRequestData
    response_type = XfersPurchaseCreateResponse


class XfersSellQuotationCreateApi(RailsRestApi):
    path = "xfers/sell/quotation/create"
    method = HttpMethods.POST
    request_data_type = XfersSellQuotationCreateRequestData
    response_type = XfersSellQuotationCreateResponse


class XfersSellCreateApi(RailsRestApi):
    path = "xfers/sell/create"
    method = HttpMethods.POST
    request_data_type = XfersSellCreateRequestData
    response_type = XfersSellCreateResponse


class FiatWalletsTransactionsApi(RailsRestApi):
    """Get fiat wallet transactions."""

    path = "fiat_wallets/transactions"
    method = HttpMethods.GET
    request_params_type = FiatWalletsTransactionsQueryParams
    response_type = FiatWalletsTransactionsResponse


class ExchangesQuotationCreateApi(RailsRestApi):
    path = "fiat/exchanges/quotation/create"
    method = HttpMethods.POST
    request_data_type = ExchangesQuotationCreateRequest
    response_type = ExchangesQuotationCreateResponse


class DcBankGetOccupationApi(RailsRestApi):
    """Get list of occupation for Canada Dc Bank application"""

    path = "ca_dcbank_application/occupations"
    method = HttpMethods.GET
    response_type = DcBankGetOccupationResponse


class DcBankGetSourceOfFundsApi(RailsRestApi):
    """Get list of source of funds for Canada Dc Bank application"""

    path = "ca_dcbank_application/source_of_funds"
    method = HttpMethods.GET
    response_type = DcBankGetSourceOfFundsResponse


class DcBankSelectOccupationApi(RailsRestApi):
    """Select occupation for Canada Dc Bank application"""

    path = "ca_dcbank_application/occupation"
    method = HttpMethods.POST
    request_data_type = DcBankSelectOccupationRequestData
    response_type = DcBankSelectOccupationResponse


class DcBankSelectSourceOfFundsApi(RailsRestApi):
    """Select source of funds for Canada Dc Bank application"""

    path = "ca_dcbank_application/source_of_funds"
    method = HttpMethods.POST
    request_data_type = DcBankSelectSourceOfFundsRequestData
    response_type = DcBankSelectSourceOfFundsResponse


class DcBankGetAddressApi(RailsRestApi):
    """Get address from Canada Dc Bank application"""

    path = "ca_dcbank_application/address"
    method = HttpMethods.GET
    response_type = DcBankGetAddressResponse


class DcBankSubmitAddressApi(RailsRestApi):
    """Submit address for Canada Dc Bank application"""

    path = "ca_dcbank_application/address"
    method = HttpMethods.POST
    request_data_type = DcBankSubmitAddressRequestData
    response_type = DcBankSubmitAddressResponse


class DcBankSubmitApplicationApi(RailsRestApi):
    """Submit Canada Dc Bank application"""

    path = "ca_dcbank_application"
    method = HttpMethods.POST
    response_type = DcBankSubmitApplicationResponse


class DcBankApplicationAddressProofApi(RailsRestApi):
    """Submit Canada Dc Bank application"""

    path = "ca_dcbank_application/address_proof"
    method = HttpMethods.POST
    request_data_type = DcBankApplicationAddressProofRequestData
    response_type = DcBankApplicationAddressProofResponse


class CADFiatDepositByReferenceNumberOverviewApi(RailsRestApi):
    """Get Canada Fiat Wallet Deposit by Reference Number Overview"""

    path = "ca_interac_etransfer/overview"
    method = HttpMethods.GET
    response_type = CADFiatDepositByReferenceNumberOverviewResponse


class CADFiatDepositCreateApi(RailsRestApi):
    """Create Canada Fiat Wallet Deposit by Reference Number"""

    path = "ca_dcbank/deposits/create"
    method = HttpMethods.POST
    request_data_type = CADFiatDepositCreateRequestData
    response_type = CADFiatDepositCreateResponse


# uk fps
class FPSSubmitAddressApi(RailsRestApi):
    """Submit FPS Address"""

    path = "v1/fiat_wallets/application/address"
    method = HttpMethods.POST
    request_data_type = UKFPSSubmitAddressRequestData
    response_type = UKFPSSubmitAddressResponse


# BRL Fiat
class BancoPluralApplicationApi(RailsRestApi):
    path = "banco_plural_application"
    method = HttpMethods.GET
    response_type = BancoPluralApplicationResponse


class BancoPluralApplicationGetAddressApi(RailsRestApi):
    path = "banco_plural_application/address"
    method = HttpMethods.GET
    response_type = BancoPluralApplicationAddressResponse


class BancoPluralApplicationCPFApi(RailsRestApi):
    path = "banco_plural_application/cpf"
    method = HttpMethods.POST
    request_data_type = BancoPluralApplicationCPFData
    response_type = BancoPluralApplicationCPFResponse


class BancoPluralApplicationAddressApi(RailsRestApi):
    path = "banco_plural_application/address"
    method = HttpMethods.POST
    response_data_type = BancoPluralApplicationAddressData
    response_type = BancoPluralApplicationAddressResponse


# SG Fast Fiat
class FiatApplicationApi(RailsRestApi):
    """Fiat Wallet Application used by SG Fast only for now."""

    path = "v1/crypto_fiat_wallets/applications"
    method = HttpMethods.POST
    request_data_type = FiatApplicationRequestData
    response_type = FiatApplicationResponse


class FiatApplicationsShowApi(RailsRestApi):
    """Fiat Wallet Application used by SG Fast only for now."""

    path = "v1/crypto_fiat_wallets/applications"
    method = HttpMethods.GET
    request_params_type = FiatApplicationsQueryParams
    response_type = FiatApplicationsShowResponse


class FiatApplicationTermsApproveApi(RailsRestApi):
    """Approve Terms and Condition for Fiat Wallet Application used by SG Fast & ARS Debin."""

    def path(self, path_params: FiatApplicationTermsApprovePathParams):
        return f"v1/crypto_fiat_wallets/applications/{path_params.application_id}/terms"

    method = HttpMethods.POST
    response_type = FiatApplicationResponse


class FiatApplicationSubmitIdentityDocumentApi(RailsRestApi):
    """Submit Identity Document for Fiat Wallet Application used by ARS Debin."""

    def path(self, path_params: FiatApplicationSubmitIdentityDocumentPathParams):
        return f"v1/crypto_fiat_wallets/applications/{path_params.application_id}/identity_document"

    request_data_type = FiatApplicationSubmitIdentityDocumentRequestData
    method = HttpMethods.POST
    response_type = FiatApplicationResponse


class FiatApplicationAddBankAccountApi(RailsRestApi):
    """Link bank account for Fiat Wallet Application used by ARS Debin."""

    def path(self, path_params: FiatApplicationAddBankAccountPathParams):
        return f"v1/crypto_fiat_wallets/applications/{path_params.application_id}/fiat_bank_account"

    request_data_type = FiatApplicationAddBankAccountRequestData
    method = HttpMethods.POST
    response_type = FiatApplicationResponse


class USDCSwiftStatusShowApi(RailsRestApi):
    """Show usdc swift status api"""

    path = "usdc_swift/status"
    method = HttpMethods.GET
    response_type = USDCSwiftStatusShowResponse


class USDCSwiftBankAccountActivateApi(RailsRestApi):
    """Activate usdc swift api"""

    path = "v1/crypto_fiat_wallets/applications"
    method = HttpMethods.POST
    request_data_type = USDCSwiftBankAccountActivateRequestData
    response_type = USDCSwiftBankAccountActivateResponse


class USDCSwiftBankAccountShowApi(RailsRestApi):
    """USDC Swift Bank account show"""

    def path(self, path_params: USDCBankAccountPathParams):
        return f"v1/crypto_fiat_wallets/applications/{path_params.application_id}/bank_account"

    method = HttpMethods.GET
    response_type = USDCSwiftBankAccountShowResponse


class USDCSwiftBankAccountCreateApi(RailsRestApi):
    """USDC Swift Bank account details create"""

    def path(self, path_params: USDCBankAccountPathParams):
        return f"v1/crypto_fiat_wallets/applications/{path_params.application_id}/bank_account"

    method = HttpMethods.POST
    request_data_type = USDCSwiftBankAccountCreateRequestData
    response_type = USDCSwiftBankAccountCreateResponse


class USDCSwiftBankAccountAddressCreateApi(RailsRestApi):
    """USDC Swift Bank account address create"""

    def path(self, path_params: USDCBankAccountPathParams):
        return f"v1/crypto_fiat_wallets/applications/{path_params.application_id}/address"

    method = HttpMethods.POST
    request_data_type = USDCSwiftBankAccountCreateAddressRequestData
    response_type = USDCSwiftBankAccountCreateAddressResponse


class USDCSwiftBankAccountProofApi(RailsRestApi):
    def path(self, path_params: USDCBankAccountPathParams):
        return f"v1/crypto_fiat_wallets/applications/{path_params.application_id}/bank_account_proof"

    method = HttpMethods.POST
    request_data_type = USDCSwiftBankAccountProofRequestData
    response_type = USDCSwiftBankAccountCreateResponse


class VibanBankInfoEmailApi(RailsRestApi):
    """Viban Bank InfoE mail Api"""

    path = "viban/bank_info/mail"
    method = HttpMethods.POST
    request_data_type = VibanBankInfoEmailRequestData
    response_type = VibanBankInfoEmailResponse


class VibanCryptoWithdrawalBeneficiariesApi(RailsRestApi):
    path = "v1/crypto_fiats/crypto_withdrawals/beneficiaries"

    method = HttpMethods.GET
    request_params_type = VibanCryptoWithdrawalBeneficiariesQueryParams
    response_type = VibanCryptoWithdrawalBeneficiariesResponse


class VibanCryptoWithdrawalOrderCreateApi(RailsRestApi):
    path = "v1/crypto_fiats/crypto_withdrawals/orders/create"
    method = HttpMethods.POST
    request_data_type = VibanCryptoWithdrawalOrderCreateRequestData
    response_type = VibanCryptoWithdrawalOrderCreateResponse


class VibanCryptoWithdrawalCreateApi(RailsRestApi):
    path = "v1/crypto_fiats/crypto_withdrawals/create"
    method = HttpMethods.POST
    request_data_type = VibanCryptoWithdrawalCreateRequestData
    response_type = VibanCryptoWithdrawalCreateResponse


class DepositRequestsOverviewApi(RailsRestApi):
    path = "v1/crypto_fiats/deposit_requests/overview"
    method = HttpMethods.GET
    request_params_type = DepositRequestsOverviewQueryParams
    response_type = DepositRequestsOverviewResponse


class DepositRequestsApi(RailsRestApi):
    path = "v1/crypto_fiats/deposit_requests"
    method = HttpMethods.POST
    request_data_type = DepositRequestsRequestData
    response_type = DepositRequestsResponse


class FiatBankAccountsApi(RailsRestApi):
    def path(self, path_params: FiatBankAccountsPathParams):
        # fmt: off
        paths = path_params.dict(exclude_none=True)
        if "payment_network" not in paths:
            return f"v1/crypto_fiats/bank_accounts?currency={path_params.currency}"
        return f"v1/crypto_fiats/bank_accounts?currency={path_params.currency}&payment_network={path_params.payment_network}"   # noqa
        # fmt: on

    method = HttpMethods.GET
    response_type = FiatBankAccountsResponse


class FiatDeleteBankAccountsApi(RailsRestApi):
    def path(self, path_params: FiatDeleteBankAccountsPathParams):
        return f"v1/crypto_fiats/bank_accounts/{path_params.id}"

    method = HttpMethods.DELETE
    response_type = FiatDeleteBankAccountResponse


class FiatBankAccountsSubmitProofApi(RailsRestApi):
    def path(self, path_params: FiatBankAccountsIdPathParams):
        return f"v1/crypto_fiats/bank_accounts/{path_params.id}/submit_proof"

    method = HttpMethods.POST
    request_data_type = FiatBankAccountsSubmitProofRequestData
    response_type = FiatBankAccountsSubmitProofResponse


class FiatWalletsApplicationShowApi(RailsRestApi):
    path = "v1/fiat_wallets/application"
    method = HttpMethods.GET
    request_params_type = FiatWalletsApplicationShowQueryParams
    response_type = FiatWalletsApplicationResponse


class UKFPSSubmitAddressProofApi(RailsRestApi):
    path = "v1/fiat_wallets/application/address_proof"
    method = HttpMethods.POST
    request_params_type = UKFPSSubmitAddressProofRequestData
    response_type = UKFPSSubmitAddressProofResponse


class FiatApplicationCountriesApi(RailsRestApi):
    """Fiat Wallet Application Countries"""

    path = "v1/fiat_wallets/application/countries"
    method = HttpMethods.GET
    request_params_type = FiatWalletsApplicationShowQueryParams
    response_type = FiatWalletApplicationCountriesResponse


class FiatApplicationPrefillAddressApi(RailsRestApi):
    """Get Fiat Wallet Application Prefill Address"""

    path = "v1/fiat_wallets/application/address"
    method = HttpMethods.GET
    request_params_type = FiatWalletsApplicationShowQueryParams
    response_type = FiatWalletApplicationPrefillAddressResponse


class FiatService(RailsRestService):
    def _submit_fps_address(
        self,
        postcode: str,
        house_number: str,
        street_name: str,
        address: str,
        province: str,
        city: str,
    ) -> UKFPSSubmitAddressResponse:
        api = FPSSubmitAddressApi(host=self.host, _session=self.session)
        data = UKFPSSubmitAddressRequestData(
            payment_network="uk_fps",
            vendor_id="bcb",
            address=UKFPSSubmitAddressRequestData.Address(
                postcode=postcode,
                address_3=street_name,
                province=province,
                address_2=house_number,
                city=city,
                country="GBR",
                address_1=address,
            ),
        ).dict(exclude_none=True)

        response = api.call(json=data)
        return UKFPSSubmitAddressResponse.parse_raw(b=response.content)

    def _accept_viban_terms(self) -> VibanTermsAcceptResponse:
        api = VibanTermsAcceptApi(host=self.host, _session=self.session)
        data = VibanTermsAcceptRequestData(
            currency="GBP",
            viban_type="uk_fps",
            term_id="use_viban_agreement",
        ).dict(exclude_none=True)

        response = api.call(json=data)
        return VibanTermsAcceptResponse.parse_raw(b=response.content)

    def add_gbp_fiat_wallet(self, terms_accept_action: str = "default"):
        if terms_accept_action == "default":
            self._accept_viban_terms()
        else:
            self._deposit_methods_terms_accept(
                term_id="use_viban_agreement",
                currency="GBP",
                deposit_methods=["uk_fps"],
            )
        self._submit_fps_address(
            postcode="11111",
            house_number="20",
            street_name="Street",
            address="Address",
            province="State",
            city="London",
        )

    def deposit_methods_show(self, currency: str) -> CryptoFiatDepositMethodsShowResponse:
        api = CryptoFiatDepositMethodsShowApi(host=self.host, _session=self.session)
        path_params = CryptoFiatDepositMethodsShowPathParams(currency=currency)
        query_params = CryptoFiatDepositMethodsShowQueryParams(currency=currency)

        response = api.call(path_params=path_params, params=query_params)
        return CryptoFiatDepositMethodsShowResponse.parse_raw(b=response.content)

    def _deposit_methods_terms_accept(
        self,
        term_id: str,
        currency: str,
        deposit_methods: List[str],
    ) -> CryptoFiatDepositMethodsTermsAcceptResponse:
        api = CryptoFiatDepositMethodsTermsAcceptApi(host=self.host, _session=self.session)
        data = CryptoFiatDepositMethodsTermsAcceptRequestData(
            term_id=term_id,
            currency=currency,
            deposit_methods=deposit_methods,
        ).dict(exclude_none=True)

        response = api.call(json=data)
        return CryptoFiatDepositMethodsTermsAcceptResponse.parse_raw(b=response.content)

    def _us_van_application_address_update(
        self,
        country: str,
        city: str,
        address_1: str,
        state_code: str,
        zip_code: str,
    ) -> USVanApplicationAddressUpdateResponse:
        api = USVanApplicationAddressUpdateApi(host=self.host, _session=self.session)
        data = USVanApplicationAddressUpdateRequestData(
            address=Address(
                country=country,
                city=city,
                address_1=address_1,
                state_code=state_code,
                zip_code=zip_code,
            )
        ).dict(exclude_none=True)

        response = api.call(json=data)
        return USVanApplicationAddressUpdateResponse.parse_raw(b=response.content)

    # TODO: using encryption method other than passcode, need to ask BE team.
    def _us_van_application_update(self, ssn: Optional[str] = None) -> USVanApplicationUpdateResponse:
        api = USVanApplicationUpdateApi(host=self.host, _session=self.session)
        data = USVanApplicationUpdateRequestData(
            ssn9="REV5NWNGNU9uWncvVG9YS09uSVdpWmVqQ2FHbVltSkI2NmRKcGJVTkZTV1ExaW5ZcTJrTUIwbitaVmZ1TTVncS0tSlNCY1hZZ1RYZ0UwbHBiNk95alUwZz09--79ebf1d4f323dffdcac9a0046a548aeab856e08c",  # noqa: E501
        ).dict(exclude_none=True)

        response = api.call(data=data)
        return USVanApplicationUpdateResponse.parse_raw(b=response.content)

    def add_usd_fiat_wallet(
        self,
        city: str = "testing city",
        address_1: str = "testing address",
        state_code: str = "CA",
        zip_code: str = "00000",
    ):
        """Add USD Fiat Wallet to user account.

        Args:
            city: user city name
            address_1: user address
            state_code: user
            zip_code:

        Returns:
            None
        """

        fiat_wallet = FiatWalletInfo(fiat=Fiat.USD)
        self._deposit_methods_terms_accept(
            term_id=fiat_wallet.term_id,
            deposit_methods=fiat_wallet.deposit_methods,
            currency=fiat_wallet.fiat.value,
        )
        self._us_van_application_address_update(
            country="USA",
            city=city,
            address_1=address_1,
            state_code=state_code,
            zip_code=zip_code,
        )
        self._us_van_application_update()

    def ach_withdrawal_bank_accounts_create(
        self,
        account_id: str,
        plaid_public_token: str,
        institution_name: str = "Citibank Online",
    ) -> ACHWithdrawalBankAccountsCreateResponse:
        api = ACHWithdrawalBankAccountsCreateApi(host=self.host, _session=self.session)
        data = ACHWithdrawalBankAccountsCreateRequestData(
            account_id=account_id,
            plaid_public_token=plaid_public_token,
            institution_name=institution_name,
        ).dict(exclude_none=True)

        response = api.call(json=data)
        return ACHWithdrawalBankAccountsCreateResponse.parse_raw(b=response.content)

    def ach_withdrawal_bank_accounts(self) -> ACHWithdrawalBankAccountsResponse:
        api = ACHWithdrawalBankAccountsApi(host=self.host, _session=self.session)

        response = api.call()
        return ACHWithdrawalBankAccountsResponse.parse_raw(b=response.content)

    def ach_withdrawal_withdrawal_create(
        self,
        bank_account_id: str,
        amount: Union[str, int, Decimal],
    ) -> ACHWithdrawalWithdrawalCreateResponse:
        api = ACHWithdrawalWithdrawalCreateApi(host=self.host, _session=self.session)
        data = ACHWithdrawalWithdrawalCreateRequestData(
            bank_account_id=bank_account_id,
            amount=str(amount),
        ).dict(exclude_none=True)

        response = api.call(json=data)
        return ACHWithdrawalWithdrawalCreateResponse.parse_raw(b=response.content)

    def ach_withdrawal_withrawal_verify_passcode(
        self,
        withdrawal_id: str,
        passcode: str,
    ) -> ACHWithdrawalWithdrawalVerifyPasscodeResponse:
        api = ACHWithdrawalWithdrawalVerifyPasscodeApi(host=self.host, _session=self.session)
        data = ACHWithdrawalWithdrawalVerifyPasscodeRequestData(
            withdrawal_id=withdrawal_id,
            passcode=passcode,
        ).dict(exclude_none=True)

        response = api.call(json=data)
        return ACHWithdrawalWithdrawalVerifyPasscodeResponse.parse_raw(b=response.content)

    def _xfers_tnc_create(self) -> XfersTNCCreateResponse:
        api = XfersTNCCreateApi(host=self.host, _session=self.session)
        data = XfersTNCCreateRequestData().dict(exclude_none=True)

        response = api.call(data=data)
        return XfersTNCCreateResponse.parse_raw(b=response.content)

    def _xfers_connect(self) -> XfersConnectResponse:
        api = XfersConnectApi(host=self.host, _session=self.session)
        data = XfersConnectRequestData().dict(exclude_none=True)

        response = api.call(data=data)
        return XfersConnectResponse.parse_raw(b=response.content)

    def add_sgd_xfers_fiat_wallet(self):
        self._xfers_tnc_create()
        self._xfers_connect()

    def _deposit_methods_terms_create(
        self,
        currency: str,
        deposit_methods: List[str],
    ) -> CryptoFiatDepositMethodsCreateResponse:
        api = CryptoFiatDepositMethodsCreateApi(host=self.host, _session=self.session)
        data = CryptoFiatDepositMethodsCreateRequestData(
            currency=currency,
            deposit_methods=deposit_methods,
        ).dict(exclude_none=True)

        response = api.call(json=data)
        return CryptoFiatDepositMethodsCreateResponse.parse_raw(b=response.content)

    def add_eur_fiat_wallet(self):
        fiat_wallet = FiatWalletInfo(fiat=Fiat.EUR)
        self._deposit_methods_terms_accept(
            term_id=fiat_wallet.term_id,
            deposit_methods=fiat_wallet.deposit_methods,
            currency=fiat_wallet.fiat.value,
        )
        self._deposit_methods_terms_create(currency=fiat_wallet.fiat.value, deposit_methods=fiat_wallet.deposit_methods)

    def add_aud_fiat_wallet(self):
        fiat_wallet = FiatWalletInfo(fiat=Fiat.AUD)
        self._deposit_methods_terms_accept(
            term_id=fiat_wallet.term_id,
            deposit_methods=fiat_wallet.deposit_methods,
            currency=fiat_wallet.fiat.value,
        )
        self._deposit_methods_terms_create(currency=fiat_wallet.fiat.value, deposit_methods=fiat_wallet.deposit_methods)

    def viban_account_summary(self) -> VibanAccountSummaryResponse:
        api = VibanAccountSummaryApi(host=self.host, _session=self.session)
        response = api.call()
        return VibanAccountSummaryResponse.parse_raw(b=response.content)

    def viban_purchases_quotation_create(
        self,
        to_amount: Union[int, str, Decimal],
        from_currency: str,
        to_currency: str,
    ) -> VibanPurchasesQuotationCreateResponse:
        api = VibanPurchasesQuotationCreateApi(host=self.host, _session=self.session)
        data = VibanPurchasesQuotationCreateRequestData(
            to_amount=str(to_amount),
            from_currency=from_currency,
            to_currency=to_currency,
        ).dict(exclude_none=True)

        response = api.call(json=data)
        return VibanPurchasesQuotationCreateResponse.parse_raw(b=response.content)

    def viban_purchases_create(self, quotation_id: str, passcode: str) -> VibanPurchasesCreateResponse:
        api = VibanPurchasesCreateApi(host=self.host, _session=self.session)
        data = VibanPurchasesCreateRequestData(quotation_id=quotation_id, passcode=passcode).dict(exclude_none=True)

        response = api.call(json=data)
        return VibanPurchasesCreateResponse.parse_raw(b=response.content)

    def viban_sell_quotation_create(
        self,
        from_currency: str,
        from_amount: Union[str, int, Decimal],
        to_currency: str,
    ) -> VibanSellQuotationCreateResponse:
        api = VibanSellQuotationCreateApi(host=self.host, _session=self.session)
        data = VibanSellQuotationCreateRequestData(
            from_currency=from_currency,
            from_amount=str(from_amount),
            to_currency=to_currency,
        ).dict(exclude_none=True)

        response = api.call(json=data)
        return VibanSellQuotationCreateResponse.parse_raw(b=response.content)

    def viban_sell_create(self, quotation_id: str, passcode: str) -> VibanSellCreateResponse:
        api = VibanSellCreateApi(host=self.host, _session=self.session)
        data = VibanSellCreateRequestData(quotation_id=quotation_id, passcode=passcode).dict(exclude_none=True)

        response = api.call(json=data)
        return VibanSellCreateResponse.parse_raw(b=response.content)

    def viban_withdrawal_beneficiaries(
        self, currency: str = "EUR", viban_type: str = "sepa"
    ) -> VibanWithdrawalBeneficiariesResponse:
        api = VibanWithdrawalBeneficiariesApi(host=self.host, _session=self.session)
        query_params = VibanWithdrawalBeneficiariesQueryParams(currency=currency, viban_type=viban_type).dict(
            exclude_none=True
        )

        response = api.call(params=query_params)
        return VibanWithdrawalBeneficiariesResponse.parse_raw(b=response.content)

    def post_viban_withdrawal_beneficiaries(
        self,
        plaid_public_token: str,
        bank_name: str,
        account_identifier_value: str,
    ) -> PostVibanWithdrawalBeneficiariesResponse:
        api = PostVibanWithdrawalBeneficiariesApi(host=self.host, _session=self.session)
        data = PostVibanWithdrawalBeneficiariesRequestData(
            plaid_public_token=plaid_public_token,
            bank_name=bank_name,
            account_identifier_value=account_identifier_value,
        ).dict(exclude_none=True)

        response = api.call(data=data)
        return PostVibanWithdrawalBeneficiariesResponse.parse_raw(b=response.content)

    def viban_withdrawal_orders_create(
        self,
        beneficiary_id: str,
        amount: Union[str, int, Decimal],
        currency: str = "EUR",
        viban_type: str = "sepa",
    ) -> VibanWithdrawalOrdersCreateResponse:
        api = VibanWithdrawalOrdersCreateApi(host=self.host, _session=self.session)
        data = VibanWithdrawalOrdersCreateRequestData(
            beneficiary_id=beneficiary_id,
            amount=str(amount),
            currency=currency,
            viban_type=viban_type,
        ).dict(exclude_none=True)

        response = api.call(json=data)
        return VibanWithdrawalOrdersCreateResponse.parse_raw(b=response.content)

    def xfers_account_show(self) -> XfersAccountShowResponse:
        api = XfersAccountShowApi(host=self.host, _session=self.session)
        response = api.call()
        return XfersAccountShowResponse.parse_raw(b=response.content)

    def xfers_purchases_quotation_create(
        self,
        to_amount: Union[int, str, Decimal],
        from_currency: str,
        to_currency: str,
    ) -> XfersPurchaseQuotationCreateResponse:
        api = XfersPurchaseQuotationCreateApi(host=self.host, _session=self.session)
        data = XfersPurchaseQuotationCreateRequestData(
            to_amount=str(to_amount),
            from_currency=from_currency,
            to_currency=to_currency,
        ).dict(exclude_none=True)

        response = api.call(json=data)
        return XfersPurchaseQuotationCreateResponse.parse_raw(b=response.content)

    def xfers_purchases_create(self, quotation_id: str, passcode: str) -> XfersPurchaseCreateResponse:
        api = XfersPurchaseCreateApi(host=self.host, _session=self.session)
        data = XfersPurchaseCreateRequestData(quotation_id=quotation_id, passcode=passcode).dict(exclude_none=True)

        response = api.call(json=data)
        return XfersPurchaseCreateResponse.parse_raw(b=response.content)

    def xfers_sell_quotation_create(
        self,
        from_amount: Union[int, str, Decimal],
        from_currency: str,
        to_currency: str,
    ) -> XfersSellQuotationCreateResponse:
        api = XfersSellQuotationCreateApi(host=self.host, _session=self.session)
        data = XfersSellQuotationCreateRequestData(
            from_amount=str(from_amount),
            from_currency=from_currency,
            to_currency=to_currency,
        ).dict(exclude_none=True)

        response = api.call(json=data)
        return XfersSellQuotationCreateResponse.parse_raw(b=response.content)

    def xfers_sell_create(self, quotation_id: str, passcode: str) -> XfersSellCreateResponse:
        api = XfersSellCreateApi(host=self.host, _session=self.session)
        data = XfersSellCreateRequestData(quotation_id=quotation_id, passcode=passcode).dict(exclude_none=True)

        response = api.call(json=data)
        return XfersSellCreateResponse.parse_raw(b=response.content)

    def fiat_wallets_transactions(self, count: int = 1) -> FiatWalletsTransactionsResponse:
        api = FiatWalletsTransactionsApi(host=self.host, _session=self.session)
        params = FiatWalletsTransactionsQueryParams(count=count).dict(exclude_none=True)

        response = api.call(params=params)
        return FiatWalletsTransactionsResponse.parse_raw(b=response.content)

    def exchanges_quotation_create(self, from_amount: str, from_side: str, to: str) -> ExchangesQuotationCreateResponse:
        api = ExchangesQuotationCreateApi(host=self.host, _session=self.session)
        data = ExchangesQuotationCreateRequest(from_amount=from_amount, from_side=from_side, to=to)

        response = api.call(json=data)
        return ExchangesQuotationCreateResponse.parse_raw(b=response.content)

    def cad_dc_bank_application_terms_accept(self):
        fiat_wallet = FiatWalletInfo(fiat=Fiat.CAD)
        self._deposit_methods_terms_accept(
            term_id=fiat_wallet.term_id,
            deposit_methods=fiat_wallet.deposit_methods,
            currency=fiat_wallet.fiat.value,
        )

    def cad_dc_bank_application_get_occupations(self) -> DcBankGetOccupationResponse:
        api = DcBankGetOccupationApi(host=self.host, _session=self.session)
        response = api.call()
        return DcBankGetOccupationResponse.parse_raw(b=response.content)

    def cad_dc_bank_application_bank_select_occupation(
        self, require_specification: bool, key: str, translation_key: str, specification: str = None
    ) -> DcBankSelectOccupationResponse:
        api = DcBankSelectOccupationApi(host=self.host, _session=self.session)
        data = DcBankSelectOccupationRequestData(
            occupation=DcBankSelectOccupationRequestData.Occupation(
                require_specification=require_specification,
                key=key,
                specification=specification,
                translation_key=translation_key,
            ).dict(exclude_none=True)
        ).dict(exclude_none=True)

        response = api.call(json=data)
        return DcBankSelectOccupationResponse.parse_raw(b=response.content)

    def cad_dc_bank_application_get_source_of_funds(self) -> DcBankGetSourceOfFundsResponse:
        api = DcBankGetSourceOfFundsApi(host=self.host, _session=self.session)
        response = api.call()
        return DcBankGetSourceOfFundsResponse.parse_raw(b=response.content)

    def cad_dc_bank_application_select_source_of_funds(
        self, source_of_funds: List[str]
    ) -> DcBankSelectSourceOfFundsResponse:
        api = DcBankSelectSourceOfFundsApi(host=self.host, _session=self.session)
        data = DcBankSelectSourceOfFundsRequestData(source_of_funds=source_of_funds).dict(exclude_none=True)

        response = api.call(json=data)
        return DcBankSelectSourceOfFundsResponse.parse_raw(b=response.content)

    def cad_dc_bank_application_get_address(self) -> DcBankGetAddressResponse:
        api = DcBankGetAddressApi(host=self.host, _session=self.session)
        response = api.call()
        return DcBankGetAddressResponse.parse_raw(b=response.content)

    def cad_dc_bank_application_submit_address(
        self, address_1: str, city: str, country: str, province: str, zip_code: str, province_key: str
    ) -> DcBankSubmitAddressResponse:
        api = DcBankSubmitAddressApi(host=self.host, _session=self.session)
        data = DcBankSubmitAddressRequestData(
            address=DcBankSubmitAddressRequestData.Address(
                address_1=address_1,
                city=city,
                country=country,
                province=province,
                zip_code=zip_code,
            ).dict(exclude_none=True),
            province_key=province_key,
        ).dict(exclude_none=True)

        response = api.call(json=data)
        return DcBankSubmitAddressResponse.parse_raw(b=response.content)

    def cad_dc_bank_application_submit(self) -> DcBankSubmitApplicationResponse:
        api = DcBankSubmitApplicationApi(host=self.host, _session=self.session)
        response = api.call()
        return DcBankSubmitApplicationResponse.parse_raw(b=response.content)

    def get_cad_fiat_deposit_by_reference_number_overview(self) -> CADFiatDepositByReferenceNumberOverviewResponse:
        api = CADFiatDepositByReferenceNumberOverviewApi(host=self.host, _session=self.session)
        response = api.call()
        return CADFiatDepositByReferenceNumberOverviewResponse.parse_raw(b=response.content)

    def cad_viban_add_withdrawal_email(
        self,
        email: str,
        phone: str,
        first_name: str,
        last_name: str,
    ) -> PostVibanWithdrawalBeneficiariesResponse:
        api = PostVibanWithdrawalBeneficiariesApi(host=self.host, _session=self.session)
        data = PostVibanWithdrawalBeneficiariesRequestData(
            phone=phone,
            account_holder_name_last_name=last_name,
            account_holder_name_first_name=first_name,
            account_identifier_value=email,
            payment_network="ca_interac_etransfer",
            currency="CAD",
            account_identifier_type="email",
        ).dict(exclude_none=True)

        response = api.call(data=data)
        return PostVibanWithdrawalBeneficiariesResponse.parse_raw(b=response.content)

    def cad_create_deposit_by_reference_number(self, reference_number: str) -> CADFiatDepositCreateResponse:
        api = CADFiatDepositCreateApi(host=self.host, _session=self.session)
        data = CADFiatDepositCreateRequestData(reference_number=reference_number).dict(exclude_none=True)
        response = api.call(data=data)
        return CADFiatDepositCreateResponse.parse_raw(b=response.content)

    def _cad_viban_withdrawal_orders_create(
        self,
        beneficiary_id: str,
        amount: Union[str, int, Decimal],
        currency: str = "CAD",
        viban_type: str = "ca_interac_etransfer",
        security_question: str = "What city were you born in?",
        security_answer: str = "Toronto",
    ) -> VibanWithdrawalOrdersCreateResponse:
        api = VibanWithdrawalOrdersCreateApi(host=self.host, _session=self.session)
        data = VibanWithdrawalOrdersCreateRequestData(
            beneficiary_id=beneficiary_id,
            amount=str(amount),
            currency=currency,
            viban_type=viban_type,
            security_question=security_question,
            security_answer=security_answer,
        ).dict(exclude_none=True)

        response = api.call(data=data)
        return VibanWithdrawalOrdersCreateResponse.parse_raw(b=response.content)

    def viban_withdrawal_create(self, order_id: str, passcode: str, otp: str) -> VibanWithdrawalCreateResponse:
        api = VibanWithdrawalCreateApi(host=self.host, _session=self.session)
        data = VibanWithdrawalCreateRequestData(order_id=order_id, passcode=passcode, otp=otp).dict(exclude_none=True)

        response = api.call(json=data)
        return VibanWithdrawalCreateResponse.parse_raw(b=response.content)

    def viban_withdrawal_create_no_otp(self, order_id: str, passcode: str) -> VibanWithdrawalCreateResponse:
        api = VibanWithdrawalCreateApi(host=self.host, _session=self.session)
        data = VibanWithdrawalCreateNoOtpRequestData(order_id=order_id, passcode=passcode).dict(exclude_none=True)

        response = api.call(json=data)
        return VibanWithdrawalCreateResponse.parse_raw(b=response.content)

    def cad_fiat_add_withdrawal(self, beneficiary_id: str, amount: Union[str, int, Decimal], passcode: str, otp: str):
        order_id = self._cad_viban_withdrawal_orders_create(
            beneficiary_id=beneficiary_id, amount=amount
        ).viban_withdrawal_order.id

        self.viban_withdrawal_create(order_id=order_id, passcode=passcode, otp=otp)

    def _get_banco_plural_application(self) -> BancoPluralApplicationResponse:
        api = BancoPluralApplicationApi(host=self.host, _session=self.session)
        response = api.call()
        return BancoPluralApplicationResponse.parse_raw(b=response.content)

    def _banco_plural_application_cpf(self, cpf: str = CPF.generate()) -> BancoPluralApplicationCPFResponse:
        api = BancoPluralApplicationCPFApi(host=self.host, _session=self.session)
        data = BancoPluralApplicationCPFData(cpf=cpf, is_triggered_by_card_flow=True).dict(exclude_none=True)

        response = api.call(json=data)
        return BancoPluralApplicationCPFResponse.parse_raw(b=response.content)

    def _banco_plural_application_address(
        self,
        house_name_and_number: str,
        county: str,
        neighborhood: str,
        state_code: str,
        street: str,
        street_number: str,
        zip_code: str,
    ) -> BancoPluralApplicationAddressResponse:
        api = BancoPluralApplicationAddressApi(host=self.host, _session=self.session)
        data = BancoPluralApplicationAddressData(
            address=BancoPluralApplicationAddressData.Address(
                complement=house_name_and_number,
                county=county,
                neighborhood=neighborhood,
                state_code=state_code,
                street=street,
                street_number=street_number,
                zip_code=zip_code,
            )
        ).dict(exclude_none=True)

        response = api.call(json=data)
        return BancoPluralApplicationAddressResponse.parse_raw(b=response.content)

    def add_brl_fiat_wallet(
        self,
        house_name_and_number: str = "house 1234",
        county: str = "county",
        neighborhood: str = "neighborhood",
        state_code: str = "AC",
        street: str = "street",
        street_number: str = "street no",
        zip_code: str = "00000000",
    ):
        """Add BRL Fiat Wallet to user account.

        Args:
            house_name_and_number: House name and number
            county: county
            neighborhood: neighborhood
            state_code: State short code, e.g. AC for Acre
            street: street
            street_number: street number
            zip_code: zip code in 8 digits

        Returns:
            None
        """

        fiat_wallet = FiatWalletInfo(fiat=Fiat.BRL)
        self._deposit_methods_terms_accept(
            term_id=fiat_wallet.term_id,
            deposit_methods=fiat_wallet.deposit_methods,
            currency=fiat_wallet.fiat.value,
        )

        # state=pending_cpf
        self._get_banco_plural_application()
        cpf_number = CPF.generate()
        self._banco_plural_application_cpf(cpf_number)
        # state=pending_address
        self._get_banco_plural_application()
        try:
            self._banco_plural_application_address(
                house_name_and_number,
                county,
                neighborhood,
                state_code,
                street,
                street_number,
                zip_code,
            )
        except RailsResponseError:
            # Will encounter `cpf_name_error` for the first time calling the api, but can proceed
            pass

        return cpf_number

    def _create_sg_fast_application(self) -> FiatApplicationResponse:
        api = FiatApplicationApi(host=self.host, _session=self.session)
        data = FiatApplicationRequestData(currency="SGD").dict(exclude_none=True)
        response = api.call(json=data)
        return FiatApplicationResponse.parse_raw(b=response.content)

    def _create_ars_debin_application(self) -> FiatApplicationResponse:
        api = FiatApplicationApi(host=self.host, _session=self.session)
        data = FiatApplicationRequestData(currency="ARS").dict(exclude_none=True)
        response = api.call(json=data)
        return FiatApplicationResponse.parse_raw(b=response.content)

    def _create_try_debin_application(self) -> FiatApplicationResponse:
        api = FiatApplicationApi(host=self.host, _session=self.session)
        data = FiatApplicationRequestData(currency="TRY").dict(exclude_none=True)
        response = api.call(json=data)
        return FiatApplicationResponse.parse_raw(b=response.content)

    def _submit_identity_document_ars_debin_application(
        self, application_id: str, cuil: str
    ) -> FiatApplicationResponse:
        api = FiatApplicationSubmitIdentityDocumentApi(host=self.host, _session=self.session)
        path_params = FiatApplicationSubmitIdentityDocumentPathParams(application_id=application_id)
        data = FiatApplicationSubmitIdentityDocumentRequestData(
            identity_document=FiatApplicationSubmitIdentityDocumentRequestData.IdentityDocument(cuil=cuil)
        ).dict(exclude_none=True)
        response = api.call(json=data, path_params=path_params)
        return FiatApplicationResponse.parse_raw(b=response.content)

    def submit_address_ars_debin_application(
        self,
        application_id: str,
        address_1: str,
        city: str,
        country: str,
        zipcode: str,
        province: str,
    ) -> FiatApplicationResponse:
        api = USDCSwiftBankAccountAddressCreateApi(host=self.host, _session=self.session)
        path_params = USDCBankAccountPathParams(application_id=application_id)
        data = USDCSwiftBankAccountCreateAddressRequestData(
            address=ApplicationAddress(
                address_1=address_1,
                city=city,
                country=country,
                zipcode=zipcode,
                province=province,
            )
        ).dict(exclude_none=True)

        response = api.call(path_params=path_params, json=data)
        return FiatApplicationResponse.parse_raw(b=response.content)

    def add_bank_account_ars_debin_application(
        self, application_id: str, account_identifier_value: str, account_identifier_type: str, account_holder_name: str
    ) -> FiatApplicationResponse:
        api = FiatApplicationAddBankAccountApi(host=self.host, _session=self.session)
        path_params = FiatApplicationAddBankAccountPathParams(application_id=application_id)
        data = FiatApplicationAddBankAccountRequestData(
            fiat_bank_account=FiatApplicationAddBankAccountRequestData.FiatBankAccount(
                account_identifier_value=account_identifier_value,
                account_identifier_type=account_identifier_type,
                account_holder_name=account_holder_name,
            )
        ).dict(exclude_none=True)
        response = api.call(path_params=path_params, json=data)
        return FiatApplicationResponse.parse_raw(b=response.content)

    def _approve_fiat_wallet_application_terms(self, application_id: str) -> FiatApplicationResponse:
        api = FiatApplicationTermsApproveApi(host=self.host, _session=self.session)
        path_params = FiatApplicationTermsApprovePathParams(application_id=application_id)

        response = api.call(path_params=path_params)
        return FiatApplicationResponse.parse_raw(b=response.content)

    def get_sg_fast_account_number(self) -> str:
        api = CryptoFiatDepositMethodsShowApi(host=self.host, _session=self.session)
        path_params = CryptoFiatDepositMethodsShowPathParams(currency="SGD", deposit_method="sg_fast")

        response = api.call(path_params=path_params)
        parsed_response = CryptoFiatDepositMethodsShowResponse.parse_raw(b=response.content)
        sg_fast_deposit_method = next(filter(lambda x: x.deposit_method == "sg_fast", parsed_response.deposit_methods))
        bank_details = next(filter(lambda x: x.key == "bank_account_number", sg_fast_deposit_method.bank_details))
        return bank_details.value

    def add_sg_fast_fiat_wallet(self):
        @retry(RailsResponseError, tries=3, delay=5)
        def approve_sg_fast_application_terms():
            application_id = self._create_sg_fast_application().application.id
            response = self._approve_fiat_wallet_application_terms(application_id)
            if response.application.verification_step not in ["pending_deposit"]:
                raise RailsResponseError("Verification step must be Pending Deposit")

        approve_sg_fast_application_terms()

    def usdc_swift_status_show(self) -> USDCSwiftStatusShowResponse:
        api = USDCSwiftStatusShowApi(host=self.host, _session=self.session)

        response = api.call()
        return USDCSwiftStatusShowResponse.parse_raw(b=response.content)

    def fiat_applications_show(self, currency: str) -> FiatApplicationsShowResponse:
        api = FiatApplicationsShowApi(host=self.host, _session=self.session)
        params = FiatApplicationsQueryParams(currency=currency).dict(exclude_none=True)

        response = api.call(params=params)
        return FiatApplicationsShowResponse.parse_raw(b=response.content)

    def usdc_swift_bank_account_show(self, application_id: str = None) -> USDCSwiftBankAccountShowResponse:
        if not application_id:
            application_id = self.fiat_applications_show("USDC").applications[0].id
        api = USDCSwiftBankAccountShowApi(host=self.host, _session=self.session)
        path_params = USDCBankAccountPathParams(application_id=application_id)

        response = api.call(path_params=path_params)
        return USDCSwiftBankAccountShowResponse.parse_raw(b=response.content)

    def usdc_swift_bank_account_activate(self, currency: str) -> USDCSwiftBankAccountActivateResponse:
        api = USDCSwiftBankAccountActivateApi(host=self.host, _session=self.session)
        data = USDCSwiftBankAccountActivateRequestData(currency=currency).dict(exclude_none=True)

        response = api.call(json=data)
        return USDCSwiftBankAccountActivateResponse.parse_raw(b=response.content)

    def usdc_swift_bank_account_create(
        self,
        application_id: str,
        account_identifier_type: str,
        account_identifier_value: str,
        bank_account_holder_name: str,
        bank_city: str = None,
        bank_country: str = None,
        bank_identifier_type: str = None,
        bank_identifier_value: str = None,
        bank_name: str = None,
        phone_country: str = "HKG",
    ) -> USDCSwiftBankAccountCreateResponse:
        api = USDCSwiftBankAccountCreateApi(host=self.host, _session=self.session)
        path_params = USDCBankAccountPathParams(application_id=application_id)

        if phone_country == "HKG":
            bank_account = USDCSwiftBankAccountCreateRequestData.InputBankAccount(
                account_identifier_type=account_identifier_type,
                account_identifier_value=account_identifier_value,
                bank_account_holder_name=bank_account_holder_name,
                bank_city=bank_city,
                bank_country=bank_country,
                bank_identifier_type=bank_identifier_type,
                bank_identifier_value=bank_identifier_value,
                bank_name=bank_name,
            )
        elif phone_country == "POL":
            bank_account = USDCSwiftBankAccountCreateRequestData.InputBankAccount(
                account_identifier_type=account_identifier_type,
                account_identifier_value=account_identifier_value,
                bank_account_holder_name=bank_account_holder_name,
            )
        else:
            raise NotImplementedError
        data = USDCSwiftBankAccountCreateRequestData(bank_account=bank_account).dict(exclude_none=True)

        response = api.call(path_params=path_params, json=data)
        return USDCSwiftBankAccountCreateResponse.parse_raw(b=response.content)

    def usdc_swift_bank_account_address_create(
        self,
        application_id: str,
        address_1: str,
        city: str,
        country: str,
        postcode: str,
        province: str,
        address_2: str,
        address_3: str,
    ) -> USDCSwiftBankAccountCreateAddressResponse:
        api = USDCSwiftBankAccountAddressCreateApi(host=self.host, _session=self.session)
        path_params = USDCBankAccountPathParams(application_id=application_id)
        data = USDCSwiftBankAccountCreateAddressRequestData(
            address=ApplicationAddress(
                address_1=address_1,
                city=city,
                country=country,
                postcode=postcode,
                province=province,
                address_2=address_2,
                address_3=address_3,
            )
        ).dict(exclude_none=True)

        response = api.call(path_params=path_params, json=data)
        return USDCSwiftBankAccountCreateAddressResponse.parse_raw(b=response.content)

    def usdc_swift_bank_account_proof(
        self,
        application_id: str,
        proof_scan_reference_id: str = None,
    ) -> USDCSwiftBankAccountCreateResponse:
        api = USDCSwiftBankAccountProofApi(host=self.host, _session=self.session)
        path_params = USDCBankAccountPathParams(application_id=application_id)

        if proof_scan_reference_id:
            data = USDCSwiftBankAccountProofRequestData(proof_scan_reference=proof_scan_reference_id).dict(
                exclude_none=True
            )
        else:
            data = USDCSwiftBankAccountProofRequestData().dict(exclude_none=True)

        response = api.call(path_params=path_params, json=data)
        return USDCSwiftBankAccountCreateResponse.parse_raw(b=response.content)

    def send_bank_info_mail(
        self, currency: str, viban_type: str, application_id: str = None
    ) -> VibanBankInfoEmailResponse:
        api = VibanBankInfoEmailApi(host=self.host, _session=self.session)
        if application_id:
            data = VibanBankInfoEmailRequestData(
                currency=currency,
                viban_type=viban_type,
                application_id=application_id,
            ).dict(exclude_none=True)
        else:
            data = VibanBankInfoEmailRequestData(
                currency=currency,
                viban_type=viban_type,
            ).dict(exclude_none=True)

        response = api.call(json=data)
        return VibanBankInfoEmailResponse.parse_raw(b=response.content)

    def crypto_withdrawal_beneficiaries(
        self, currency: str, viban_type: str
    ) -> VibanCryptoWithdrawalBeneficiariesResponse:
        api = VibanCryptoWithdrawalBeneficiariesApi(host=self.host, _session=self.session)
        query_params = VibanCryptoWithdrawalBeneficiariesQueryParams(currency=currency, viban_type=viban_type)

        response = api.call(params=query_params)
        return VibanCryptoWithdrawalBeneficiariesResponse.parse_raw(b=response.content)

    def viban_crypto_withdrawal_orders_create(
        self,
        beneficiary_id: str,
        amount: Union[str, int, Decimal],
        currency: str = "USDC",
        viban_type: str = "usdc_swift",
    ) -> VibanCryptoWithdrawalOrderCreateResponse:
        api = VibanCryptoWithdrawalOrderCreateApi(host=self.host, _session=self.session)
        data = VibanCryptoWithdrawalOrderCreateRequestData(
            beneficiary_id=beneficiary_id,
            amount=str(amount),
            currency=currency,
            viban_type=viban_type,
        ).dict(exclude_none=True)

        response = api.call(json=data)
        return VibanCryptoWithdrawalOrderCreateResponse.parse_raw(b=response.content)

    def viban_crypto_withdrawal_create(
        self, order_id: str, passcode: str, otp: str
    ) -> VibanCryptoWithdrawalCreateResponse:
        api = VibanCryptoWithdrawalCreateApi(host=self.host, _session=self.session)
        data = VibanCryptoWithdrawalCreateRequestData(order_id=order_id, passcode=passcode, otp=otp).dict(
            exclude_none=True
        )

        response = api.call(json=data)
        return VibanCryptoWithdrawalCreateResponse.parse_raw(b=response.content)

    def viban_crypto_withdrawal_create_no_otp(
        self, order_id: str, passcode: str
    ) -> VibanCryptoWithdrawalCreateResponse:
        api = VibanCryptoWithdrawalCreateApi(host=self.host, _session=self.session)
        data = VibanCryptoWithdrawalCreateNotOtpRequestData(order_id=order_id, passcode=passcode).dict(
            exclude_none=True
        )

        response = api.call(json=data)
        return VibanCryptoWithdrawalCreateResponse.parse_raw(b=response.content)

    def deposit_requests_overview(self, currency: str, payment_network: str) -> DepositRequestsOverviewResponse:
        api = DepositRequestsOverviewApi(host=self.host, _session=self.session)
        query_params = DepositRequestsOverviewQueryParams(currency=currency, payment_network=payment_network)

        response = api.call(params=query_params)
        return DepositRequestsOverviewResponse.parse_raw(b=response.content)

    def deposit_requests_create(
        self, currency: str, payment_network: str, bank_account_id: str, amount: str, passcode: str
    ) -> DepositRequestsResponse:
        api = DepositRequestsApi(host=self.host, _session=self.session)
        data = DepositRequestsRequestData(
            payment_network=payment_network,
            bank_account_id=bank_account_id,
            amount=amount,
            currency=currency,
            passcode=passcode,
        ).dict(exclude_none=True)

        response = api.call(json=data)
        return DepositRequestsResponse.parse_raw(b=response.content)

    def get_fiat_bank_accounts(self, currency: str, payment_network: str) -> FiatBankAccountsResponse:
        api = FiatBankAccountsApi(host=self.host, _session=self.session)
        path_params = FiatBankAccountsPathParams(currency=currency, payment_network=payment_network)

        response = api.call(path_params=path_params)
        return FiatBankAccountsResponse.parse_raw(b=response.content)

    def delete_fiat_bank_account(self, id: str) -> FiatDeleteBankAccountResponse:
        api = FiatDeleteBankAccountsApi(host=self.host, _session=self.session)
        path_params = FiatDeleteBankAccountsPathParams(id=id)
        response = api.call(path_params=path_params)
        return FiatDeleteBankAccountResponse.parse_raw(b=response.content)

    def add_ars_debin_fiat_wallet(
        self,
        cuil: str = "12345678912",
        address_1: str = "ABCDE",
        city: str = "Ensenada",
        province: str = "BA",
        zipcode: str = "A1234ABC",
        country: str = "Argentina",
        account_number: str = "2850590940090418135203",
        account_type: str = "CBU",
        account_holder_name: str = "Tudor Stark",
    ):
        @retry(RailsResponseError, tries=3, delay=5)
        def accept_ars_debin_application_terms(application_id: str):
            response = self._approve_fiat_wallet_application_terms(application_id)
            if response.application.verification_step not in ["pending_identity_document"]:
                raise RailsResponseError("Verification step must be Pending Identity Document")

        @retry(RailsResponseError, tries=3, delay=5)
        def submit_ars_debin_application_identity_document(application_id: str, cuil: str):
            response = self._submit_identity_document_ars_debin_application(application_id=application_id, cuil=cuil)
            if response.application.verification_step not in ["pending_address"]:
                raise RailsResponseError("Verification step must be Pending Address")

        @retry(RailsResponseError, tries=3, delay=5)
        def submit_ars_debin_application_address(
            application_id: str, address_1: str, city: str, province: str, country: str, zipcode: str
        ):
            response = self.submit_address_ars_debin_application(
                application_id, address_1=address_1, city=city, province=province, country=country, zipcode=zipcode
            )
            if response.application.verification_step not in ["pending_review"]:
                raise RailsResponseError("Verification step must be Pending Review")

        @retry(RailsResponseError, tries=3, delay=5)
        def add_ars_debin_application_bank_account(
            application_id: str, account_number: str, account_type: str, account_holder_name: str
        ):
            response = self.add_bank_account_ars_debin_application(
                application_id=application_id,
                account_identifier_value=account_number,
                account_identifier_type=account_type,
                account_holder_name=account_holder_name,
            )
            if response.application.verification_step not in ["fiat_bank_account_submitted"]:
                raise RailsResponseError("Verification step must be Fiat Bank Account Submitted")

        @retry(RailsResponseError, tries=20, delay=15)
        def wait_document_approved():
            response = self.fiat_applications_show(currency="ARS")
            for application in response.applications:
                if application.verification_step == "pending_fiat_bank_account":
                    break
                else:
                    raise RailsResponseError("Verification step must be Pending Fiat Bank Account")

        @retry(RailsResponseError, tries=20, delay=15)
        def wait_application_approved():
            response = self.fiat_applications_show(currency="ARS")
            for application in response.applications:
                if application.verification_step == "completed":
                    break
                else:
                    raise RailsResponseError("Verification step must be Completed")

        application_id = self._create_ars_debin_application().application.id
        accept_ars_debin_application_terms(application_id)
        submit_ars_debin_application_identity_document(application_id, cuil)
        submit_ars_debin_application_address(application_id, address_1, city, province, country, zipcode)
        wait_document_approved()
        add_ars_debin_application_bank_account(application_id, account_number, account_type, account_holder_name)
        wait_application_approved()

    def deposit_ars_to_fiat_wallet(self, amount: str, passcode: str):
        payment_network = "ar_debin"
        currency = "ARS"
        bank_accounts = self.get_fiat_bank_accounts(currency=currency, payment_network=payment_network).bank_accounts
        for bank_account in bank_accounts:
            if bank_account.currency == currency:
                bank_account_id = bank_account.id

        return self.deposit_requests_create(
            currency=currency,
            amount=amount,
            bank_account_id=bank_account_id,
            payment_network=payment_network,
            passcode=passcode,
        )

    def fiat_wallets_application_show(self, vendor_id: str, payment_network: str) -> FiatWalletsApplicationResponse:
        api = FiatWalletsApplicationShowApi(host=self.host, _session=self.session)
        query = FiatWalletsApplicationShowQueryParams(
            vendor_id=vendor_id,
            payment_network=payment_network,
        )

        response = api.call(params=query)
        return FiatWalletsApplicationResponse.parse_raw(b=response.content)

    def uk_fps_submit_address_proof(
        self,
        proof_scan_reference_id: str = None,
    ) -> UKFPSSubmitAddressProofResponse:
        api = UKFPSSubmitAddressProofApi(host=self.host, _session=self.session)

        if proof_scan_reference_id:
            data = UKFPSSubmitAddressProofRequestData(
                proof_scan_reference=proof_scan_reference_id,
            ).dict(exclude_none=True)
        else:
            data = UKFPSSubmitAddressProofRequestData().dict(exclude_none=True)

        response = api.call(json=data)
        return UKFPSSubmitAddressProofResponse.parse_raw(b=response.content)

    def accept_try_bulut_application_terms(self):
        application_id = self._create_try_debin_application().application.id
        response = self._approve_fiat_wallet_application_terms(application_id)
        if response.application.verification_step not in ["pending_deposit"]:
            raise RailsResponseError("Verification step must be pending_deposit")

    def ca_dc_bank_address_proof_upload(self) -> DcBankApplicationAddressProofResponse:
        api = DcBankApplicationAddressProofApi(host=self.host, _session=self.session)
        data = DcBankApplicationAddressProofRequestData().dict(exclude_none=True)

        response = api.call(json=data)
        return DcBankApplicationAddressProofResponse.parse_raw(b=response.content)

    def get_fiat_wallet_application_countries(
        self,
        vendor_id: str,
        payment_network: str,
    ) -> FiatWalletApplicationCountriesResponse:
        api = FiatApplicationCountriesApi(host=self.host, _session=self.session)
        query = FiatWalletsApplicationShowQueryParams(
            vendor_id=vendor_id,
            payment_network=payment_network,
        )
        response = api.call(params=query)
        return FiatWalletApplicationCountriesResponse.parse_raw(b=response.content)

    def get_fiat_wallet_application_prefill_address(
        self,
        vendor_id: str,
        payment_network: str,
    ) -> FiatWalletApplicationPrefillAddressResponse:
        api = FiatApplicationPrefillAddressApi(host=self.host, _session=self.session)
        query = FiatWalletsApplicationShowQueryParams(
            vendor_id=vendor_id,
            payment_network=payment_network,
        )
        response = api.call(params=query)
        return FiatWalletApplicationPrefillAddressResponse.parse_raw(b=response.content)

    def submit_bank_account_proof(self, bank_account_id: str) -> FiatBankAccountsSubmitProofResponse:
        api = FiatBankAccountsSubmitProofApi(host=self.host, _session=self.session)
        path_params = FiatBankAccountsIdPathParams(id=bank_account_id)
        data = FiatBankAccountsSubmitProofRequestData().dict()

        response = api.call(path_params=path_params, json=data)
        return FiatBankAccountsSubmitProofResponse.parse_raw(b=response.content)
