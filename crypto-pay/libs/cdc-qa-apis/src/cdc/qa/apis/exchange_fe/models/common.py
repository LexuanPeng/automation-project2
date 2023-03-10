from decimal import Decimal
from typing import Dict, List, Optional, Union

from cdc.qa.apis.exchange_fe.models.finance import SymbolInfo
from pydantic import Field

from ..fe_models import FeExchangeRequest, FeExchangeResponse, FrozenBaseModel


class UserInfoRequest(FeExchangeRequest):
    pass


class UserInfoDataDetail(FrozenBaseModel):
    googleStatus: int
    sysSoftStakingOpen: int = Field(description="1 - opened, 0 - not opened")
    zeroTradingFeeDuration: int
    mobileNumber: str = Field(description="user mobile number with encrypt string")
    feeCoinRate: str
    isEnabledWithdrawalApi: int = Field(description="1 - enabled withdrawal api, 0 - disabled withdraw api")
    uuid: str = Field(description="user uuid")
    fee_coin_open: str
    lastLoginIp: str
    userTier: int
    accountStatus: int = Field(description="default is 0")
    isOpenMobileCheck: int
    userTierReinforcementEnabled: bool
    countryCode: str = Field(description="Country code. e.g. POL")
    derivativeAccountStatus: int = Field(description="Derivative Account Status, 1 - Opened; 0 - Not Opened")
    email: str = Field(description="user email")
    nickName: str = Field(description="user nick name")
    useSoftStakingOpen: int = Field(description="1 - opened, o - not opened")
    walletAppStatus: int
    isEnabledCroMainnet: int
    myMarket: List
    useFeeCoinOpen: int
    zeroTradingFeeActiveDays: int
    marginAccountStatus: int = Field(
        description="Margin Account Status, 1 - Margin Wallet is Opened, 0 - Margin Wallet is not opened"
    )
    isEligibleForMarginFeature: bool
    lastLoginTime: str
    feeCoin: str = Field(description="Fee Coin, e.g. CRO")
    phoneCountryCode: str = Field(description="Phone country code. e.g. POL")
    isEnabledZeroTradingFee: int = Field(description="0 - disabled zero trading fee, 1 - enabled zero trading fee")
    userAccount: str = Field(description="email with encrypt string")
    isEnabledDerivativeBetaProduct: int = Field(
        description="0 - disabled derivative beta product, 1 - enabled derivative beta product"
    )
    userType: int = Field(description="user type: 0 - retail, 1 - institutional")
    authLevel: int = Field(description="auth level")
    isEligibleForDerivativeFeature: bool


class UserInfoResponse(FeExchangeResponse):
    data: UserInfoDataDetail = Field(description="User info data")


# /common/supported_coins
class NetworkInfo(FrozenBaseModel):
    minWithdrawalAmount: Decimal
    withdrawalFees: Optional[Decimal]
    confirmation: int
    network: str
    address_type: Union[str, None]
    withdraw_open: Optional[int]
    deposit_open: Optional[int]
    is_xapp_released: Optional[int]
    is_public_release: Optional[int]
    address_max_length: Optional[int]
    address_pattern: Optional[str]
    networkDisplayName: Optional[str]


class SymbolInfo(FrozenBaseModel):
    fullName: str
    networks: List[NetworkInfo]
    withdrawal_decimals: int


class SymbolsInfo(FrozenBaseModel):
    __root__: Dict[str, SymbolInfo]

    def __iter__(self):
        return iter(self.__root__)

    def __getattr__(self, item):
        return self.__root__.get(item, None)


class SupportedCoinsResponseData(FrozenBaseModel):
    lastUpdatedAt: int
    symbols: SymbolsInfo


class SupportedCoinsResponse(FeExchangeResponse):
    data: SupportedCoinsResponseData
