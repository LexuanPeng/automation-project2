from decimal import Decimal
from typing import List, Optional

from cdc.qa.apis.exchange.models import ExchangeResponse, ExchangeSignedRequest, FrozenBaseModel
from pydantic import Field


class GetSubAccountParams(FrozenBaseModel):
    page_size: Optional[int] = Field(description="Page size (Default 20, max 100)")


class GetSubAccountRequestBody(ExchangeSignedRequest):
    method: str = "private/subaccount/get-sub-accounts"
    params: GetSubAccountParams = Field()


class SubAccountDetail(FrozenBaseModel):
    uuid: str = Field(description="Sub account uuid")
    master_account_uuid: str = Field(description="Master account uuid")
    margin_account_uuid: Optional[str] = Field(description="Margin account uuid")
    derivatives_account_uuid: Optional[str] = Field(description="Derivatives account uuid")
    label: Optional[str] = Field(description="Sub account label")
    enabled: bool = Field(description="true or false")
    tradable: bool = Field(description="true or false")
    name: str = Field(description="Name of sub account")
    email: str = Field(description="Email of sub account")
    mobile_number: str = Field(description="Mobile number of sub account")
    country_code: str = Field(description="Country Code of sub account")
    address: str = Field(description="Address of sub account")
    margin_access: str = Field(description="DEFAULT or DISABLED")
    derivatives_access: str = Field(description="DEFAULT or DISABLED")
    create_time: int = Field(description="Creation timestamp")
    update_time: int = Field(description="Last update timestamp")
    two_fa_enabled: bool = Field(description="true or false")
    kyc_level: str = Field(description="Kyc Level")
    suspended: bool = Field(description="true or false")
    terminated: bool = Field(description="true or false")


class GetSubAccountResult(FrozenBaseModel):
    sub_account_list: List[SubAccountDetail] = Field()


class GetSubAccountsResponse(ExchangeResponse):
    result: GetSubAccountResult = Field()


class GetTransferHistoryRequestParams(FrozenBaseModel):
    sub_account_uuid: str = Field(description="sub account uuid")
    direction: str = Field(description="Transfer direction into or out of Account E.g. IN or OUT")
    currency: Optional[str] = Field(description="Currency being transferred E.g. BTC, CRO or omit for 'all'")
    start_ts: Optional[int] = Field(description="Default is 24 hours ago from current timestamp")
    end_ts: Optional[int] = Field(description="Default is current timestamp")
    page_size: Optional[int] = Field(description="Page size (Default: 20, Max: 200)")
    page: Optional[int] = Field(description="Page number (0-based)")


class GetTransferHistoryBody(ExchangeSignedRequest):
    method: str = "private/subaccount/get-transfer-history"
    params: GetTransferHistoryRequestParams = Field()


class TransferHistoryDetail(FrozenBaseModel):
    direction: str = Field(description="Transfer direction into or out of Account E.g. IN or OUT")
    time: int = Field(description="Transfer creation time (Unix timestamp)")
    amount: Decimal = Field(description="Amount transferred")
    status: str = Field(description="Indicates status of the transfer")
    information: str = Field(description="Text description of the transfer")
    currency: str = Field(description="Currency E.g. BTC, USDT")
    sub_account_uuid: str = Field()
    sub_account_label: str = Field()
    transfer_from: str = Field(description="MASTER or SUBACCOUNT", alias="from")
    from_wallet: str = Field(description="SPOT or MARGIN")
    to: str = Field(description="MASTER or SUBACCOUNT")
    to_wallet: str = Field(description="SPOT or MARGIN")


class GetTransferHistoryResult(FrozenBaseModel):
    transfer_list: List[TransferHistoryDetail] = Field(description="transfer list response")


class GetTransferHistoryResponse(ExchangeResponse):
    result: GetTransferHistoryResult = Field()


class TransferRequestParams(FrozenBaseModel):
    currency: str = Field(description="Transfer currency, e.g. BTC, CRO")
    transfer_from: str = Field(description="MASTER or SUBACCOUNT", alias="from")
    from_wallet: Optional[str] = Field(description="SPOT or MARGIN (Default: SPOT)")
    to: str = Field("MASTER or SUBACCOUNT")
    to_wallet: Optional[str] = Field(description="SPOT or MARGIN (Default: SPOT)")
    sub_account_uuid: str = Field()
    amount: str = Field(description="The amount to be transferred")


class TransferRequestBody(ExchangeSignedRequest):
    method: str = "private/subaccount/transfer"
    params: TransferRequestParams = Field()


class TransferResponse(FrozenBaseModel):
    id: Optional[int] = Field()
    code: int = Field()
