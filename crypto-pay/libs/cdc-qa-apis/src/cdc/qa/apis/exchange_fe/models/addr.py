from ..fe_models import FeExchangeRequest, FeExchangeResponse, FrozenBaseModel
from pydantic import Field
from typing import List, Optional


# addr/address_list
class AddressListRequest(FeExchangeRequest):
    coinSymbol: Optional[str] = Field(description="coin symbol. e.g:CELR")


class CoinInfo(FrozenBaseModel):
    coinShow: str
    coinSymbol: str


class AddressDetail(FrozenBaseModel):
    address: str
    ctime: int
    fingerprint: str
    id: int
    label: str
    status: int
    symbol: str
    tokenBase: Optional[str] = Field(default=None)
    trustType: int
    uid: Optional[int] = Field(default=None)


class AddressListDataDetail(FrozenBaseModel):
    addressList: List[AddressDetail]
    cryptoCoinList: List[CoinInfo]


class AddressListResponse(FeExchangeResponse):
    data: AddressListDataDetail = Field(description="Create Margin Account Response")


# addr/add_withdraw_addr
class AddWithdrawAddrRequest(FeExchangeRequest):
    coinSymbol: str = Field(description="coin symbol. e.g:CELR")
    network: str
    address: str
    label: str
    smsOtp: str
    googleCode: str
    memo: Optional[str]
    destinationTag: Optional[str]
    isOwnerOfAddress: bool = Field(default=True)
    recipientName: str = Field(default="")
    addressTypeId: int = Field(default=2)


class AddWithdrawAddrResponse(FeExchangeResponse):
    pass


# addr/delete_withdraw_addr
class DeleteWithdrawAddrRequest(FeExchangeRequest):
    ids: List[int]
    smsOtp: str
    googleCode: str


class DeleteWithdrawAddrResponse(FeExchangeResponse):
    data: List[AddressDetail]
