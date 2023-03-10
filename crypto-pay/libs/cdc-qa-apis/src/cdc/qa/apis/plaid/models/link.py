from typing import Optional, List

from cdc.qa.apis.plaid.models import FrozenBaseModel
from pydantic import Field


# ItemCreate
class ItemCreateRequestData(FrozenBaseModel):
    class Credentials(FrozenBaseModel):
        username: str = Field(default="user_good")
        password: str = Field(default="pass_good")

    class Options(FrozenBaseModel):
        class LinkConfiguration(FrozenBaseModel):
            class UserConfig(FrozenBaseModel):
                env: str = Field(default="sandbox")
                isMobile: bool = Field(default=True)
                isWebview: bool = Field(default=False)
                isIosSdkInProcessWebview: bool = Field(default=False)
                linkSdkVersion: str = Field(default="2.1.1")
                token: str = Field(default="link-sandbox-32d02937-db78-4d27-a016-dbc495a9bd94")
                experimentVariants: dict = Field(default={})
                product: List[str] = Field(default=["auth", "identity"])
                webhook: Optional[str] = Field(default=None)
                countryCodes: List[str] = Field(default=["US"])
                language: str = Field(default="en")
                clientName: str = Field(default="Crypto.com")
                accountSubtypes: str = Field(default=None)
                paymentToken: str = Field(default=None)
                institutionId: str = Field(default=None)
                isInitializedWithLinkToken: str = Field(default=None)
                optionalProducts: list = Field(default=[])
                microdepositsEnabledOverride: bool = Field(default=False)
                oauthRedirectUri: str = Field(default="https://st.mona.co/magic/plaid/setup")
                publicToken: Optional[str] = Field(default=None)
                apiVersion: str = Field(default="v2")
                customizations: Optional[str] = Field(default=None)

            class SelectedInstitution(FrozenBaseModel):
                class Products(FrozenBaseModel):
                    auth: bool = Field(default=True)
                    connect: bool = Field(default=True)
                    income: bool = Field(default=True)
                    info: bool = Field(default=True)
                    account_verify: bool = Field(default=True)
                    assets: bool = Field(default=True)
                    bank_transfer: bool = Field(default=False)
                    transfer: bool = Field(default=False)
                    ddta: bool = Field(default=False)
                    deposit_switch: bool = Field(default=False)
                    holdings: bool = Field(default=False)
                    income_verification: bool = Field(default=False)
                    investments_auth: bool = Field(default=False)
                    investments: bool = Field(default=False)
                    liabilities: bool = Field(default=True)
                    payment_initiation: bool = Field(default=False)
                    sba_verification: bool = Field(default=False)
                    liabilities_report: bool = Field(default=False)

                accountLocked: str = Field(default="https://online.citibank.com/US/JSO/signon/uname/Next.do")
                accountSetup: str = Field(default="https://online.citibank.com")
                brandName: str = Field(default="Citibank Online")
                brandSubheading: Optional[str] = Field(default=None)
                colors: dict = Field(
                    default={
                        "dark": "#1a3469",
                        "darker": "#00174f",
                        "light": "#3f579b",
                        "primary": "#204081",
                    }
                )
                fields: List[dict] = Field(
                    default=[
                        {"label": "User ID", "name": "username", "type": "text"},
                        {"label": "Password", "name": "password", "type": "password"},
                    ]
                )
                forgottenPassword: str = Field(
                    default="https://online.citibank.com/US/JSO/uidn/RequestUserIDReminder.do"
                )
                healthStatus: str = Field(default="HEALTH_STATUS_GREEN")
                highlightReason: Optional[str] = Field(default="")
                id: str = Field(default="citi")
                inputSpec: str = Field(default="fixed")
                legacyInstitutionCode: Optional[str] = Field(default=None)
                legacyInstitutionCodeOrType: str = Field(default="citi")
                legacyInstitutionType: str = Field(default="citi")
                logo: str = Field(
                    default="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"  # noqa: E501
                )
                mfaCodeType: str = Field(default="numeric")
                name: str = Field(default="Citi")
                nameBreak: Optional[str] = Field(default=None)
                oauth: bool = Field(default=False)
                oauthLoginUrl: Optional[str] = Field(default=None)
                isNoResponseFlexInput: bool = Field(default=False)
                products: Products = Field(default_factory=Products)
                type: str = Field(default="citi")
                url: str = Field(default="https://www.citi.com")
                countryCodes: List[str] = Field(default=["US"])
                mobileAuth: bool = Field(default=False)
                filterType: str = Field(default="FILTER_TYPE_NULL")

            version: str = Field(default="1.0")
            userConfig: UserConfig = Field(default_factory=UserConfig)
            selectedInstitution: SelectedInstitution = Field(default_factory=SelectedInstitution)
            isCustomInitializer: bool = Field(default=False)
            isPatch: bool = Field(default=False)

        link_configuration: LinkConfiguration = Field(default_factory=LinkConfiguration)
        use_public_token_nonce: bool = Field(default=False)

    link_token: str = Field()
    credentials: Credentials = Field(default_factory=Credentials)
    flexible_input_responses: Optional[str] = Field(default=None)
    initial_products: List[str] = Field(default=["auth", "identity"])
    institution_id: str = Field(default="ins_5")
    link_open_id: str = Field(default="1ee4a607-82cf-4381-b2bc-4c20c4a0fcc8")
    link_persistent_id: str = Field(default="94ead043-2592-49cc-8552-8db0ab9e6c0a")
    link_session_id: str = Field(default="3a362890-e4fd-459b-8350-3a8b7864b13e")
    display_language: str = Field(default="en")
    options: Options = Field(default_factory=Options)
    payment_token: Optional[str] = Field(default=None)
    integration_mode: int = Field(default=3)
    link_sdk_version: str = Field(default="2.1.1")


class ItemCreateResponse(FrozenBaseModel):
    class Account(FrozenBaseModel):
        class Balances(FrozenBaseModel):
            class Localized(FrozenBaseModel):
                available: str
                current: str

            available: float
            currency: str
            current: float
            localized: Localized

        account_id: str
        balances: Balances
        mask: str
        name: str
        subtype: str
        type: str

    accounts: List[Account] = Field()
    public_token: str = Field()
    request_id: str = Field()
