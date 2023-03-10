from typing import List, Optional, Union, Dict
from decimal import Decimal
from cdc.qa.apis.exchange.models import ExchangeResponse, ExchangeSignedRequest, FrozenBaseModel
from pydantic import Field

"""
include API:
private/margin/get-user-config
private/margin/get-account-summary
private/margin/transfer
private/margin/borrow
private/margin/repay
private/margin/get-transfer-history
private/margin/get-borrow-history
private/margin/get-repay-history
"""


# private/margin/get-user-config
class GetUserConfigRequestBody(ExchangeSignedRequest):
    method: str = "private/margin/get-user-config"
    params: Dict = Field()


class GetUserConfigCurrencyConfigsDetail(FrozenBaseModel):
    currency: str = Field(description="E.g. BTC, USDT")
    hourly_rate: Decimal = Field(description="Hourly interest rate")
    max_borrow_limit: Decimal = Field(description="Maximum borrow limit based on collateral in the Margin Wallet")
    min_borrow_limit: Decimal = Field(description="Minimum borrow limit")


class GetUserConfigResult(FrozenBaseModel):
    stake_amount: int = Field()
    currency_configs: List[GetUserConfigCurrencyConfigsDetail] = Field()


class GetUserConfigResponse(ExchangeResponse):
    result: GetUserConfigResult = Field()


# private/margin/get-account-summary
class GetAccountSummaryRequestBody(ExchangeSignedRequest):
    method: str = "private/margin/get-account-summary"
    params: Dict = Field()


class AccountsDetail(FrozenBaseModel):
    balance: Decimal = Field()
    available: Decimal = Field(description="Available balance")
    order: Decimal = Field(description="Order balance")
    borrowed: Decimal = Field(description="Borrowed balance")
    position: Decimal
    positionHomeCurrency: Decimal
    positionBtc: Decimal
    lastPriceHomeCurrency: Decimal
    lastPriceBtc: Decimal
    currency: str = Field(description="Currency")
    accrued_interest: Decimal = Field(description="Accrued interest")
    liquidation_price: Decimal


class AccountsSummaryDetail(FrozenBaseModel):
    is_liquidating: bool = Field(description="Describes whether the account is under liquidation")
    total_balance: Decimal = Field(description="total balance")
    total_balance_btc: Decimal = Field(description="total balance BTC")
    equity_value: Decimal = Field(description="Total equity value in home currency")
    equity_value_btc: Decimal = Field(description="Total equity value in BTC currency")
    total_borrowed: Decimal = Field(description="Total borrowed")
    total_borrowed_btc: Decimal = Field(description="Total borrowed BTC")
    total_accrued_interest: Decimal = Field(description="Total Accrued interest")
    total_accrued_interest_btc: Decimal = Field(description="Total accrued interest BTCe")
    margin_ratio: Optional[Decimal] = Field()
    margin_ratio_actual: Optional[Decimal] = Field()
    margin_score: str = Field(description="GOOD, FAIR, or CRITICAL")
    currency: str = Field(description="Home currency in USDT")
    accounts: List[AccountsDetail] = Field()


class GetAccountSummaryResponse(ExchangeResponse):
    result: AccountsSummaryDetail = Field()


# private/margin/transfer
class TransferRequestParams(FrozenBaseModel):
    currency: str = Field(description="Transfer currency, e.g. USDT")
    from_side: str = Field(description="SPOT or MARGIN", alias="from")
    to: str = Field(description="SPOT or MARGIN")
    amount: Union[str, int, Decimal] = Field(description="The amount to be transferred")


class TransferRequestBody(ExchangeSignedRequest):
    method: str = "private/margin/transfer"
    params: TransferRequestParams = Field()


class TransferResponse(ExchangeResponse):
    pass


# private/margin/borrow
class BorrowRequestParams(FrozenBaseModel):
    currency: str = Field(description="Borrow currency, e.g. BTC, CRO")
    amount: Optional[Union[str, Decimal]] = Field(description="The amount to be borrowed")


class BorrowRequestBody(ExchangeSignedRequest):
    method: str = "private/margin/borrow"
    params: BorrowRequestParams = Field()


class BorrowResponse(ExchangeResponse):
    pass


# private/margin/repay
class RepayRequestParams(FrozenBaseModel):
    currency: str = Field(description="Repay currency, e.g. BTC, CRO")
    amount: Union[str, Decimal] = Field(description="The amount to be rapaid")


class RepayRequestBody(ExchangeSignedRequest):
    method: str = "private/margin/repay"
    params: RepayRequestParams = Field()


class RepayResponse(ExchangeResponse):
    pass


# private/margin/get-transfer-history
class TransferHistoryDetail(FrozenBaseModel):
    direction: str = Field(description="Transfer direction into or out of Margin Wallet E.g. IN or OUT")
    time: int = Field(description="Transfer creation time (Unix timestamp)")
    amount: Decimal = Field(description="Amount transferred")
    status: str = Field(description="Indicates status of the transfer")
    information: str = Field(description="Text description of the transfer in relation to the Spot Wallet")
    currency: str = Field(description="Currency E.g. BTC, USDT")


class GetTransferHistoryRequestParams(FrozenBaseModel):
    direction: str = Field(description="Transfer direction into or out of Margin Wallet E.g. IN or OUT")
    currency: Optional[str] = Field(default=None, description="Currency being transferred E.g. BTC or omit for 'all'")
    start_ts: Optional[int] = Field(default=None, description="Start timestamp", ge=0)
    end_ts: Optional[int] = Field(default=None, description="end timestamp", ge=0)
    page_size: Optional[int] = Field(default=None, description="Page size (Default: 20, Max: 200)", ge=0, le=200)
    page: Optional[int] = Field(default=None, description="Page number (0-based)", ge=0)


class GetTransferHistoryRequestBody(ExchangeSignedRequest):
    method: str = "private/margin/get-transfer-history"
    params: GetTransferHistoryRequestParams = Field()


class GetTransferHistoryResult(FrozenBaseModel):
    transfer_list: List[TransferHistoryDetail] = Field()


class GetTransferHistoryResponse(ExchangeResponse):
    result: GetTransferHistoryResult = Field()


# private/margin/get-borrow-history
class GetBorrowHistoryRequestParams(FrozenBaseModel):
    currency: Optional[str] = Field(description="Currency being borrowed E.g. BTC, CRO or omit for 'all'")
    start_ts: Optional[int] = Field(description="Default is 24 hours ago from current timestamp")
    end_ts: Optional[int] = Field(description="Default is current timestamp")
    page_size: Optional[int] = Field(description="Page size (Default: 20, Max: 200)")
    page: Optional[int] = Field(description="Page number (0-based)")


class GetBorrowHistoryRequestBody(ExchangeSignedRequest):
    method: str = "private/margin/get-borrow-history"
    params: GetBorrowHistoryRequestParams = Field()


class BorrowHistoryListDetail(FrozenBaseModel):
    loan_id: str = Field(description="Unique identifier for the loan")
    currency: str = Field(description="Currency E.g. BTC, USDT")
    loan_amount: Decimal = Field(description="Amount borrowed")
    borrow_time: int = Field(description="Loan creation time (Unix timestamp)")
    status: str = Field(description="Indicates status of the loan E.g. ACTIVE, PAID")


class BorrowHistoryResult(FrozenBaseModel):
    borrow_list: List[BorrowHistoryListDetail] = Field(description="Borrow List")


class GetBorrowHistoryResponse(ExchangeResponse):
    result: BorrowHistoryResult = Field()


# private/margin/get-repay-history
class GetRepayHistoryRequestParams(FrozenBaseModel):
    currency: Optional[str] = Field(description="Currency E.g. BTC, USDT")
    start_ts: Optional[int] = Field(
        description="Default is 24 hours ago from the current timestamp. Max time range is 1 month."
    )
    end_ts: Optional[int] = Field(description="Default is current timestamp")
    page_size: Optional[int] = Field(description="Page size (Default: 20, Max: 200)")
    page: Optional[int] = Field(description="Page number (0-based)")


class GetRepayHistoryRequestBody(ExchangeSignedRequest):
    method: str = "private/margin/get-repay-history"
    params: GetRepayHistoryRequestParams = Field()


class GetRepayHistoryListDetail(FrozenBaseModel):
    repay_id: str = Field(description="Unique identifier for the repayment")
    currency: str = Field(description="Currency of the repayment E.g. BTC, USDT")
    repay_amount: Decimal = Field(description="Total amount repaid")
    repay_time: int = Field(description="Time that the repaid occurred")
    status: str = Field(description="Status of the repayment E.g. CONFIRMED")
    outstanding_debt: Decimal = Field()
    principal_repayment: Decimal
    outstanding_principal: Decimal
    interest_repayment: Decimal
    outstanding_interest: Decimal
    repay_source: str


class GetRepayHistoryList(FrozenBaseModel):
    repay_list: List[GetRepayHistoryListDetail] = Field()


class GetRepayHistoryResponse(ExchangeResponse):
    result: GetRepayHistoryList = Field()


class AdjustMarginLeverageRequestParams(FrozenBaseModel):
    target_leverage: int = Field(description="Margin Leverage, it can be 3, 5, 10")


class AdjustMarginLeverageRequestBody(ExchangeSignedRequest):
    method: str = "private/margin/adjust-margin-leverage"
    params: AdjustMarginLeverageRequestParams = Field()


class AdjustMarginLeverageResponse(ExchangeResponse):
    pass


class GetMarginTradingUserRequestBody(ExchangeSignedRequest):
    method: str = "private/margin/get-margin-trading-user"
    params: Dict = Field()


class GetMarginTradingUserResult(FrozenBaseModel):
    margin_leverage: int = Field(description="Margin Leverage, it can be 3, 5, 10")


class GetMarginTradingUserResponse(ExchangeResponse):
    result: GetMarginTradingUserResult = Field()
