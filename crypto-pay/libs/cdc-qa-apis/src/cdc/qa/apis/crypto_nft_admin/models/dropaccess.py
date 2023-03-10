from typing import List, Optional

from pydantic import Field

from cdc.qa.apis.crypto_nft_admin.models import RestResponse, FrozenBaseModel


class GetDropAccessPathParams(FrozenBaseModel):
    drop_id: str = Field(description="the uuid of drop")


class GetDropAccessResponse(RestResponse):
    id: int = Field(description="the id of dropAccess")
    title: str = Field(description="the title of dropAccess")
    uuid: str = Field(description="the uuid of dropAccess")
    type: int = Field(description="the type of dropAccess")
    description: str = Field(description="the description of dropAccess")
    start_time: str = Field(description="the startTime of dropAccess, effective only when type is EarlyAccess")
    end_time: str = Field(description="the endTime of dropAccess, effective only when type is EarlyAccess")


class GetDropAccessAbnormalResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class GrantItemToDropAccessPathParams(FrozenBaseModel):
    drop_id: Optional[str] = Field(description="the uuid of drop")


class ItemList(FrozenBaseModel):
    item_id: str = Field(description="the uuid of dropAccess granted item which depends on grantType")
    type: str = Field(description="the grantType of grant item, value: 0: User, 1: Asset, 2: Collection")


class GrantItemToDropAccessDetailParams(FrozenBaseModel):
    item_list: List[ItemList] = Field(description="a array of grant item")


class GrantItemToDropAccessResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class CreateDropAccessDetailParams(FrozenBaseModel):
    description: str = Field(description="the description of dropAccess, max-length: 2048")
    title: str = Field(description="the title of dropAccess, max-length: 256")
    start_time: str = Field(
        description="""the startTime of dropAccess, required if type is EarlyAccess,
and after current time, eg.: 2022-12-12T18:30:30.222Z"""
    )
    end_time: str = Field(
        description="""the endTime of dropAccess, required if type is EarlyAccess,
and must be before drop.startTime, and after current time, eg.: 2022-12-12T18:30:30.222Z"""
    )
    drop_id: str = Field(description="the uuid of drop")
    type: int = Field(description="the AccessType of dropAcces, value: 0: EarlyAccess, 1: ExclusiveAccess")


class CreateDropAccessResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class EditDropAccessPathParams(FrozenBaseModel):
    drop_id: str = Field(description="the uuid of drop")


class EditDropAccessDetailParams(FrozenBaseModel):
    description: str = Field(description="the description of dropAccess, max-length: 2048")
    title: str = Field(description="the title of dropAccess, max-length: 256")
    start_time: str = Field(
        description="""the startTime of dropAccess, required if type is EarlyAccess,
and after current time, eg.: 2022-12-12T18:30:30.222Z"""
    )
    end_time: str = Field(
        description="""the endTime of dropAccess, required if type is EarlyAccess,
and must be before drop.startTime, and after current time, eg.: 2022-12-12T18:30:30.222Z"""
    )
    type: int = Field(description="the AccessType of dropAcces, value: 0: EarlyAccess, 1: ExclusiveAccess")


class EditDropAccessResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class UpdateDropAccessReservedCountPathParams(FrozenBaseModel):
    drop_id: str = Field(description="the uuid of drop")
    drop_item_id: str = Field(description="the uuid of drop item")


class UpdateDropAccessReservedCountDetailParams(FrozenBaseModel):
    type: int = Field(description="the type of drop item, value: 0: Collectible, 1: DropAsset, 2: Pack")
    reserved_count: int = Field(
        description="""the reservedCount of drop item,
must be less than or equal to the number of copies of drop item, min: 1"""
    )


class UpdateDropAccessReservedCountResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class DeleteConfiguredDropAccessPathParams(FrozenBaseModel):
    drop_id: str = Field(description="the uuid of drop")


class DeleteConfiguredDropAccessResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class DeleteGrantedDropAccessItemPathParams(FrozenBaseModel):
    drop_id: str = Field(description="the uuid of drop")
    item_id: str = Field(description="the itemId of grant item")


class DeleteGrantedDropAccessItemResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class CreateDropAccessDwDetailParams(FrozenBaseModel):
    description: str = Field(description="the description of dropAccess, max-length: 2048")
    title: str = Field(description="the title of dropAccess, max-length: 256")
    start_time: Optional[str] = Field(
        description="""the startTime of dropAccess, required if type is EarlyAccess,
and after current time, eg.: 2022-12-12T18:30:30.222Z"""
    )
    end_time: Optional[str] = Field(
        description="""the endTime of dropAccess, required if type is EarlyAccess,
and must be before drop.startTime, and after current time, eg.: 2022-12-12T18:30:30.222Z"""
    )
    drop_id: str = Field(description="the uuid of drop")
    type: int = Field(description="the AccessType of dropAcces, value: 0: EarlyAccess, 1: ExclusiveAccess")


class CreateDropAccessDwResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class EditDropAccessDwPathParams(FrozenBaseModel):
    drop_id: str = Field(description="the uuid of drop")


class EditDropAccessDwDetailParams(FrozenBaseModel):
    description: str = Field(description="the description of dropAccess, max-length: 2048")
    title: str = Field(description="the title of dropAccess, max-length: 256")
    start_time: Optional[str] = Field(
        description="""the startTime of dropAccess, required if type is EarlyAccess,
and after current time, eg.: 2022-12-12T18:30:30.222Z"""
    )
    end_time: Optional[str] = Field(
        description="""the endTime of dropAccess, required if type is EarlyAccess,
and must be before drop.startTime, and after current time, eg.: 2022-12-12T18:30:30.222Z"""
    )
    type: int = Field(description="the AccessType of dropAcces, value: 0: EarlyAccess, 1: ExclusiveAccess")


class EditDropAccessDwResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class UpdateDropAccessReservedCountDwPathParams(FrozenBaseModel):
    drop_id: str = Field(description="the uuid of drop")
    drop_item_id: str = Field(description="the uuid of drop item")


class UpdateDropAccessReservedCountDwDetailParams(FrozenBaseModel):
    type: int = Field(description="the type of drop item, value: 0: Collectible, 1: DropAsset, 2: Pack")
    reserved_count: int = Field(
        description="""the reservedCount of drop item,
must be less than or equal to the number of copies of drop item, min: 1"""
    )


class UpdateDropAccessReservedCountDwResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class DeleteConfiguredDropAccessDwPathParams(FrozenBaseModel):
    drop_id: str = Field(description="the uuid of drop")


class DeleteConfiguredDropAccessDwResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class DeleteGrantedDropAccessItemDwPathParams(FrozenBaseModel):
    drop_id: str = Field(description="the uuid of drop")
    item_id: str = Field(description="the itemId of grant item")


class DeleteGrantedDropAccessItemDwResponse(RestResponse):
    code: int = Field()
    message: str = Field()
