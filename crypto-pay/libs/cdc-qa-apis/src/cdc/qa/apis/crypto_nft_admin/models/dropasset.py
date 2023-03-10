from typing import List, Optional, Any

from pydantic import Field

from cdc.qa.apis.crypto_nft_admin.models import RestResponse, FrozenBaseModel


class GetDropAssetDetailParams(FrozenBaseModel):
    current_page: int = Field(description="The page number wanna to get, min: 1")
    page_size: Optional[int] = Field(default=20, description="Number of rows of the page, max: 100")
    id: Optional[str] = Field(description="the id of drop-asset")
    name: Optional[str] = Field(description="the name of drop-asset, max-length: 256")
    creator_uuids: Optional[list] = Field(default=[], description="the matching creators uuid list")


class GetDropAssetResponse(RestResponse):
    data: list = Field()
    total: int = Field()


class GetDropAssetAbnormalResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class GetDropAssetByIdPathParams(FrozenBaseModel):
    id: str = Field(description="The uuid of created drop-asset")


class GetDropAssetByIdResponse(RestResponse):
    assets: Optional[list] = Field(description="The asset list of pack")
    id: int = Field(description="The id of pack")
    collectibles: Optional[int] = Field(description="pack collectibles")
    uuid: str = Field(description="The uuid of pack")
    name: str = Field(description="The name of pack")
    description: str = Field(description="The description of pack")
    cover: Optional[Any] = Field(description="The cover of pack")
    blocked: bool = Field(description="The blocked of pack")
    collection: Optional[Any] = Field(description="The collection of pack")
    creator_info: Optional[Any] = Field(description="The creator of pack")
    drop: Optional[Any] = Field(description="The drop of pack")
    max_per_order: Optional[int] = Field(description="max purchase per order")
    max_per_user: Optional[int] = Field(description="max purchase per user")
    quantity: Optional[int] = Field(description="pack quantity")
    remark: Optional[str] = Field(description="The remark of pack")
    status: int = Field(description="The pack status")


class GetDropAssetByIdAbnormalResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class CreateDropAssetDwParams(FrozenBaseModel):
    trait: str = Field(description="The trait of property, max-length: 256")
    value: str = Field(description="The trait of value, max-length: 256")


class CreateDropAssetDwDetailParams(FrozenBaseModel):
    name: str = Field(description="the name of drop-asset, max-length: 256")
    cover: str = Field(
        description="the cover of drop-asset, a uuid which comes from system api's payload after you upload files"
    )
    main: str = Field(
        description="the main of drop-asset, a uuid which comes from system api's payload after you upload files"
    )
    type: int = Field(description="the type of drop-asset,it is a enum value, value: 0: Fixed, 1: Open")
    editions: int = Field(default=1, description="the editions of drop-asset")
    royalty: int = Field(description="the royalty of drop-asset")
    collection_id: Optional[str] = Field(description="the collection uuid of drop-asset")
    category_list: list = Field(
        default=[],
        description="the category of drop-asset,it is a array uuid which comes from category create api",
    )
    description: str = Field(description="the description of drop-asset, max-length: 256")
    creator_id: str = Field(description="the creatorId of drop-asset")
    properties: List[CreateDropAssetDwParams] = Field(
        default=[],
        description="the properties of drop-asset,it is a array Property: Inline Property",
    )
    on_chain: bool = Field(
        default=False,
        description="on chain or not of created drop-asset",
    )


class CreateDropAssetDwResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class EditDropAssetDwPathParams(FrozenBaseModel):
    id: str = Field(description="The uuid of created drop-asset")


class EditDropAssetDwDetailParams(FrozenBaseModel):
    name: str = Field(description="the name of drop-asset, max-length: 256")
    cover: Optional[str] = Field(
        description="the cover of drop-asset, a uuid which comes from system api's payload after you upload files"
    )
    main: str = Field(
        description="the main of drop-asset, a uuid which comes from system api's payload after you upload files"
    )
    type: int = Field(description="the type of drop-asset,it is a enum value, value: 0: Fixed, 1: Open")
    editions: int = Field(default=1, description="the editions of drop-asset")
    royalty: int = Field(description="the royalty of drop-asset")
    collection_id: Optional[str] = Field(description="the collection uuid of drop-asset")
    category: list = Field(
        default=[],
        description="the category of drop-asset,it is a array uuid which comes from category create api",
    )
    description: str = Field(description="the description of drop-asset, max-length: 256")
    properties: List[CreateDropAssetDwParams] = Field(
        default=[],
        description="the properties of drop-asset,it is a array Property: Inline Property",
    )
    on_chain: bool = Field(
        default=False,
        description="on chain or not of created drop-asset",
    )
    auction_max_end_date: Optional[str] = Field(
        description="the auctionMaxEndDate of drop-asset, eg.: 2022-12-12T18:30:30.222Z"
    )
    remark: Optional[str] = Field(description="the remark of drop-asset")
    blocked: Optional[bool] = Field(description="the blocked of drop-asset")
    withdrawal: Optional[bool] = Field(default=False, description="the withdrawal of drop-asset")
    showcopiesincirculation: Optional[bool] = Field(description="the showCopiesInCirculation of drop-asset")


class EditDropAssetDwResponse(RestResponse):
    code: int = Field()
    message: str = Field()
