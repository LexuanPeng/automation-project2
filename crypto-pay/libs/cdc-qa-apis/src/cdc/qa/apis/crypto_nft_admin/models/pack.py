from typing import List, Optional, Any

from pydantic import Field

from cdc.qa.apis.crypto_nft_admin.models import RestResponse, FrozenBaseModel


class GetPackDetailParams(FrozenBaseModel):
    current_page: int = Field(description="The page number wanna to get, min: 1")
    page_size: Optional[int] = Field(default=20, description="Number of rows of the page, max: 100")
    id: Optional[str] = Field(description="the id of pack")
    name: Optional[str] = Field(description="the name of pack, max-length: 256")
    creator_uuids: Optional[list] = Field(default=[], description="the matching creators uuid list")


class GetPackResponse(RestResponse):
    data: list = Field()
    total: int = Field()


class GetPackAbnormalResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class GetPackByUuidPathParams(FrozenBaseModel):
    uuid: str = Field(description="the uuid of pack")


class GetPackByUuidResponse(RestResponse):
    assets: Optional[list] = Field(description="The asset list of pack")
    id: int = Field(description="The id of pack")
    collectibles: int = Field(description="pack collectibles")
    uuid: str = Field(description="The uuid of pack")
    name: str = Field(description="The name of pack")
    description: str = Field(description="The description of pack")
    cover: Optional[Any] = Field(description="The cover of pack")
    blocked: bool = Field(description="The blocked of pack")
    collection: Optional[Any] = Field(description="The collection of pack")
    creator_info: Optional[Any] = Field(description="The creator of pack")
    drop: Optional[Any] = Field(description="The drop of pack")
    max_per_order: int = Field(description="max purchase per order")
    max_per_user: Optional[int] = Field(description="max purchase per user")
    quantity: int = Field(description="pack quantity")
    remark: Optional[str] = Field(description="The remark of pack")
    status: int = Field(description="The pack status")


class GetPackByUuidAbnormalResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class CreatePackDetailParams(FrozenBaseModel):
    name: str = Field(description="the name of pack, max-length: 256")
    description: str = Field(description="the description of pack, max-length: 500")
    creator_id: str = Field(description="the creatorId of pack")
    collectibles: int = Field(
        description="collectibles number per pack, cannot be modified if pack has attached to drop, min: 1"
    )
    asset_ids: Optional[list] = Field(
        default=[], description="the drop asset uuid list, should passed empty list if pack has attached to drop"
    )
    cover: str = Field(
        description="the cover of pack, a uuid which comes from system api's payload after you upload files"
    )
    quantity: int = Field(description="pack quantity, min: 1")
    collection_id: Optional[str] = Field(description="collection uuid of pack")


class CreatePackResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class EditPackPathParams(FrozenBaseModel):
    uuid: str = Field(description="the uuid of pack")


class EditPackDetailParams(FrozenBaseModel):
    name: str = Field(description="the name of pack, max-length: 256")
    description: str = Field(description="the description of pack, max-length: 500")
    collectibles: int = Field(
        description="collectibles number per pack, cannot be modified if pack has attached to drop, min: 1"
    )
    asset_ids: Optional[list] = Field(
        default=[], description="the drop asset uuid list, should passed empty list if pack has attached to drop"
    )
    cover: str = Field(
        description="the cover of pack, a uuid which comes from system api's payload after you upload files"
    )
    collection_id: Optional[str] = Field(description="collection uuid of pack")
    blocked: bool = Field(description="the blocked of pack")
    max_per_user: Optional[int] = Field(description="max purchase number per user, min: 1")
    max_per_order: int = Field(description="max purchase number per order, min: 1")
    remark: Optional[str] = Field(description="the remark of pack, max-length: 256")


class EditPackResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class CreatePackDWDetailParams(FrozenBaseModel):
    name: str = Field(description="the name of pack, max-length: 256")
    description: str = Field(description="the description of pack, max-length: 500")
    creator_id: str = Field(description="the creatorId of pack")
    collectibles: int = Field(
        description="collectibles number per pack, cannot be modified if pack has attached to drop, min: 1"
    )
    asset_ids: Optional[list] = Field(
        default=[], description="the drop asset uuid list, should passed empty list if pack has attached to drop"
    )
    cover: str = Field(
        description="the cover of pack, a uuid which comes from system api's payload after you upload files"
    )
    quantity: int = Field(description="pack quantity, min: 1")
    collection_id: Optional[str] = Field(description="collection uuid of pack")


class CreatePackDWResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class EditPackDWPathParams(FrozenBaseModel):
    uuid: str = Field(description="the uuid of pack")


class EditPackDWDetailParams(FrozenBaseModel):
    name: str = Field(description="the name of pack, max-length: 256")
    description: str = Field(description="the description of pack, max-length: 500")
    collectibles: int = Field(
        description="collectibles number per pack, cannot be modified if pack has attached to drop, min: 1"
    )
    asset_ids: Optional[list] = Field(
        default=[], description="the drop asset uuid list, should passed empty list if pack has attached to drop"
    )
    cover: str = Field(
        description="the cover of pack, a uuid which comes from system api's payload after you upload files"
    )
    collection_id: Optional[str] = Field(description="collection uuid of pack")
    blocked: bool = Field(description="the blocked of pack")
    max_per_user: Optional[int] = Field(description="max purchase number per user, min: 1")
    max_per_order: int = Field(description="max purchase number per order, min: 1")
    remark: Optional[str] = Field(description="the remark of pack, max-length: 256")


class EditPackDWResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class CreatePackItemsPathParams(FrozenBaseModel):
    pack_id: str = Field(description="the uuid of pack")


class CreatePackEachItemParams(FrozenBaseModel):
    item_id: str = Field(description="the item id (the uuid of drop asset or the uuid of collectible)")
    type: int = Field(description="the type of pack item,it is a enum below (value: 0 DropAsset, 1: Collectible)")


class CreatePackItemsDetailParams(FrozenBaseModel):
    items: List[CreatePackEachItemParams] = Field(default=[], description="list of items")


class CreatePackItemsResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class EditPackItemsPathParams(FrozenBaseModel):
    pack_id: str = Field(description="the uuid of pack")


class EditPackEachItemParams(FrozenBaseModel):
    item_id: str = Field(description="the item id (the uuid of drop asset or the uuid of collectible)")
    type: int = Field(description="the type of pack item,it is a enum below (value: 0 DropAsset, 1: Collectible)")


class EditPackItemsDetailParams(FrozenBaseModel):
    items: List[CreatePackEachItemParams] = Field(default=[], description="list of items")


class EditPackItemsResponse(RestResponse):
    code: int = Field()
    message: str = Field()
