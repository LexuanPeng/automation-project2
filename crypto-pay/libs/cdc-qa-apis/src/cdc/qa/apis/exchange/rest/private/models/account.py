from decimal import Decimal
from enum import Enum
from typing import List, Optional, Dict

from cdc.qa.apis.exchange.models import ExchangeResponse, ExchangeSignedRequest, FrozenBaseModel
from pydantic import Field


class AccountDetail(FrozenBaseModel):
    balance: Decimal = Field(description="Total balance")
    available: Decimal = Field(description="Available balance (e.g. not in orders, or locked, etc.)")
    order: Decimal = Field(description="Balance locked in orders")
    stake: Decimal = Field(description="Balance locked for staking (typically only used for CRO)")
    currency: str = Field(description="e.g. CRO")


# private/get-account-summary
class GetAccountSummaryRequestParams(FrozenBaseModel):
    currency: Optional[str] = Field(default=None, description="Specific currency, e.g. CRO. Omit for 'all'")


class GetAccountSummaryRequestBody(ExchangeSignedRequest):
    method: str = "private/get-account-summary"
    params: GetAccountSummaryRequestParams = Field()


class GetAccountSummaryResult(FrozenBaseModel):
    accounts: List[AccountDetail] = Field()


class GetAccountSummaryResponse(ExchangeResponse):
    result: GetAccountSummaryResult = Field()


# private/get-withdrawal-history
class WithdrawalStatus(Enum):
    """
    0 - Pending
    1 - Processing
    2 - Rejected
    3 - Payment In-progress
    4 - Payment Failed
    5 - Completed
    6 - Cancelled
    """

    PENDING = "0"
    Processing = "1"
    REJECTED = "2"
    PAYMENT_IN_PROGRESS = "3"
    PAYMENT_FAILED = "4"
    COMPLETED = "5"
    CANCELLED = "6"


class GetWithdrawalHistoryRequestParams(FrozenBaseModel):
    currency: Optional[str] = Field(description="E.g. BTC, CRO")
    start_ts: Optional[int] = Field(description="Default is 90 days from current timestamp")
    end_ts: Optional[str] = Field(description="Default is current timestamp")
    page_size: Optional[int] = Field(description="Page size (Default: 20, Max: 200)")
    page: Optional[int] = Field(description="Page number (0-based)")
    status: Optional[WithdrawalStatus] = Field(description="withdrawal status")


class GetWithdrawalHistoryRequest(ExchangeSignedRequest):
    method: str = "private/get-withdrawal-history"
    params: GetWithdrawalHistoryRequestParams = Field()


class WithdrawalDetail(FrozenBaseModel):
    id: int = Field(description="Newly created withdrawal ID")
    client_wid: str = Field(description="(Optional) if a Client withdrawal ID was provided in the request")
    currency: str = Field(description="E.g. BTC, CRO")
    amount: Decimal
    fee: Decimal
    address: str = Field(description="Address with Address Tag (if any)")
    create_time: int
    update_time: int
    status: WithdrawalStatus = Field(description="withdrawal status")
    txid: str = Field(description="Transaction hash")


class GetWithdrawalHistoryResult(FrozenBaseModel):
    withdrawal_list: List[WithdrawalDetail] = Field()


class GetWithdrawalHistoryResponse(ExchangeResponse):
    result: GetWithdrawalHistoryResult = Field()


# private/get-deposit-history
class DepositStatus(Enum):
    """
    0 - Not Arrived
    1 - Arrived
    2 - Failed
    3 - Pending
    """

    NOT_ARRIVED = "0"
    ARRIVED = "1"
    FAILED = "2"
    PENDING = "3"


class GetDepositHistoryRequestParams(FrozenBaseModel):
    currency: Optional[str] = Field(description="E.g. BTC, CRO")
    start_ts: Optional[int] = Field(description="Default is 90 days from current timestamp")
    end_ts: Optional[str] = Field(description="Default is current timestamp")
    page_size: Optional[int] = Field(description="Page size (Default: 20, Max: 200)")
    page: Optional[int] = Field(description="Page number (0-based)")
    status: Optional[DepositStatus] = Field(description="deposit status")


class GetDepositHistoryRequest(ExchangeSignedRequest):
    method: str = "private/get-deposit-history"
    params: GetDepositHistoryRequestParams = Field()


class DepositDetail(FrozenBaseModel):
    id: int = Field(description="Newly created deposit ID")
    currency: str = Field(description="(Optional) if a Client withdrawal ID was provided in the request")
    amount: Decimal
    fee: Decimal
    address: str = Field(description="Address with Address Tag (if any)")
    status: DepositStatus = Field(description="deposit status")
    txid: str = Field(default="")
    create_time: int
    update_time: int


class GetDepositHistoryResult(FrozenBaseModel):
    deposit_list: List[DepositDetail] = Field()


class GetDepositHistoryResponse(ExchangeResponse):
    result: GetDepositHistoryResult = Field()


# private/get-deposit-address
class DepositAddressStatus(Enum):
    """0 - Inactive   1 - Active"""

    INACTIVE = "0"
    ACTIVE = "1"


class GetDepositAddressRequestParams(FrozenBaseModel):
    currency: Optional[str] = Field(description="E.g. BTC, CRO")


class GetDepositAddressRequest(ExchangeSignedRequest):
    method: str = "private/get-deposit-address"
    params: GetDepositAddressRequestParams = Field()


class AddressDetail(FrozenBaseModel):
    id: int = Field(description="Newly created address ID")
    currency: str = Field(description="E.g. BTC, CRO")
    network: str = Field(description="E.g. ETH, CRO")
    address: str = Field(description="Address with Address Tag (if any)")
    create_time: int
    status: DepositAddressStatus = Field(description="""0 - Inactive   1 - Active""")


class GetDepositAddressResult(FrozenBaseModel):
    deposit_address_list: List[AddressDetail] = Field()


class GetDepositAddressResponse(ExchangeResponse):
    result: GetDepositAddressResult = Field()


# private/create-withdrawal
class CreateWithdrawalRequestParams(FrozenBaseModel):
    client_wid: Optional[str] = Field(description="Optional Client withdrawal ID")
    currency: str = Field(description="E.g. BTC, CRO")
    amount: Decimal
    address: str = Field(description="Address with Address Tag (if any)")
    address_tag: Optional[str] = Field(
        description="Secondary address identifier for coins like XRP, XLM etc. Also known as memo or tags."
    )


class CreateWithdrawalRequest(ExchangeSignedRequest):
    method: str = "private/create-withdrawal"
    params: CreateWithdrawalRequestParams = Field()


class CreateWithdrawalResult(FrozenBaseModel):
    id: int = Field(description="Newly created withdrawal ID")
    client_wid: Optional[str] = Field(description="(Optional) if a Client withdrawal ID was provided in the request")
    currency: str = Field(description="E.g. BTC, CRO, ETH")
    amount: Decimal
    fee: Decimal
    address: str = Field(description="Address with Address Tag (if any)")
    create_time: int
    network_id: Optional[str]


class CreateWithdrawalResponse(ExchangeResponse):
    result: CreateWithdrawalResult = Field()


# private/get-currency-networks
class GetCurrencyNetworksRequest(ExchangeSignedRequest):
    method: str = "private/get-currency-networks"
    params: dict = {}


class NetworkList(FrozenBaseModel):
    network_id: str = Field(description="the network id, can be used in create-withdrawal")
    withdraw_enabled: bool = Field()
    deposit_enabled: bool = Field()
    withdrawal_fee: Decimal = Field(default=None)
    min_withdrawal_amount: Decimal
    confirmation_required: int = Field(description="confirmation blocks count")


class CurrencyMapDetail(FrozenBaseModel):
    full_name: str = Field(description="e.g. SHIBA INU")
    default_network: str = Field(
        default=None,
        description="If network is not provided in create-withdrawal, it will search for default_network, "
        "if there is more than 1 network available.",
    )
    network_list: List[NetworkList] = Field(description="A list of networks")


class GetCurrencyNetworksResult(FrozenBaseModel):
    update_time: int
    currency_map: Dict[str, CurrencyMapDetail]


class GetCurrencyNetworksResponse(ExchangeResponse):
    result: GetCurrencyNetworksResult = Field()
