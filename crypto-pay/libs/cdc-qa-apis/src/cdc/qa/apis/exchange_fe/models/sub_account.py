from ..fe_models import FeExchangeRequest, FeExchangeResponse, FrozenBaseModel
from pydantic import Field
from typing import Optional


class SubAccountDataDetail(FrozenBaseModel):
    uuid: str = Field(description="Sub account uuid")
    master_account_uuid: str = Field(description="Master account uuid")
    margin_account_uuid: Optional[str] = Field(description="Margin account uuid")
    derivatives_account_uuid: Optional[str] = Field(description="Derivatives account uuid")
    label: str = Field(description="Sub account label")
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


class SuspendSubAccountParams(FrozenBaseModel):
    uuid: str = Field(description="Sub account uuid")


class SuspendSubAccountRequest(FeExchangeRequest):
    method: str = "private/subaccount/suspend-sub-account"
    params: SuspendSubAccountParams = Field()


class SuspendSubAccountResponse(FeExchangeResponse):
    result: Optional[SubAccountDataDetail] = Field(description="Suspend Sub Account Response")


class UnSuspendSubAccountParams(FrozenBaseModel):
    uuid: str = Field(description="Sub account uuid")


class UnSuspendSubAccountRequest(FeExchangeRequest):
    method: str = "private/subaccount/unsuspend-sub-account"
    params: UnSuspendSubAccountParams = Field()


class UnSuspendSubAccountResponse(FeExchangeResponse):
    result: Optional[SubAccountDataDetail] = Field(description="UnSuspend Sub Account Response")


class TerminateSubAccountParams(FrozenBaseModel):
    uuid: str = Field(description="Sub account uuid")


class TerminateSubAccountRequest(FeExchangeRequest):
    method: str = "private/subaccount/terminate-sub-account"
    params: TerminateSubAccountParams = Field()


class TerminateSubAccountResponse(FeExchangeResponse):
    result: Optional[SubAccountDataDetail] = Field(description="Terminate Sub Account Response")


class AddSubAccountParams(FrozenBaseModel):
    label: str = Field(description="Label of the sub account")
    enabled: bool = Field(description="true or false")
    tradable: bool = Field(description="true or false")
    name: Optional[str] = Field(description="Name of the sub account")
    email: Optional[str] = Field(description="Email of the sub account")
    mobile_number: Optional[str] = Field(description="Mobile number of the sub account")
    address: Optional[str] = Field(description="Address of the sub account")
    margin_access: str = Field(description="DEFAULT or DISABLED")
    derivatives_access: str = Field(description="DEFAULT or DISABLED")


class AddSubAccountRequest(FeExchangeRequest):
    method: str = "private/subaccount/add-sub-account"
    params: AddSubAccountParams = Field()


class AddSubAccountResponse(FeExchangeResponse):
    result: Optional[SubAccountDataDetail] = Field(description="Add Sub Account Response")


class UpdateSubAccountParams(FrozenBaseModel):
    uuid: str = Field(description="Sub account uuid")
    label: str = Field(description="Label of the sub account")
    enabled: bool = Field(description="true or false")
    tradable: bool = Field(description="true or false")
    margin_access: str = Field(description="DEFAULT or DISABLED")
    derivatives_access: str = Field(description="DEFAULT or DISABLED")


class UpdateSubAccountRequest(FeExchangeRequest):
    method: str = "private/subaccount/update-sub-account"
    params: UpdateSubAccountParams = Field()


class UpdateSubAccountResponse(FeExchangeResponse):
    result: Optional[SubAccountDataDetail] = Field(description="Update Sub Account Response")
