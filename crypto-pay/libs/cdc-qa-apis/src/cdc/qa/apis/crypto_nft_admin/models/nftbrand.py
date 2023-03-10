from typing import List, Optional, Any

from pydantic import Field

from cdc.qa.apis.crypto_nft_admin.models import RestResponse, FrozenBaseModel


class GetBrandListParams(FrozenBaseModel):
    current_page: int = Field(description="The page number wanna to get, min: 1")
    page_size: Optional[int] = Field(default=20, description="Number of rows of the page, max: 100")


class GetBrandListResponse(RestResponse):
    data: list = Field()
    total: int = Field()


class GetBrandListAbnormalResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class GetBrandDetailPathParams(FrozenBaseModel):
    id: int = Field(description="the uuid of brand")


class GetBrandDetailResponse(RestResponse):
    uuid: str = Field(description="The uuid of brand")
    name: str = Field(description="The name of brand")
    creator: str = Field(description="The creatorId of brand")
    slug: str = Field(description="The slug of brand")
    cover: Any = Field(description="The cover of brand")
    blocked: bool = Field(description="The block of brand")
    description: str = Field(description="The description of brand")
    collection_book_id: str = Field(description="the uuid of collection book")
    drops: list = Field(description="The dropList of brand")


class GetBrandDetailAbnormalResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class CreateBrandParams(FrozenBaseModel):
    name: str = Field(description="the name of brand, max-length: 30")
    creator_id: str = Field(description="the creatorId of brand")
    slug: str = Field(description="the slug of brand, max-length: 16")
    cover: str = Field(
        description="the cover of brand, a uuid which comes from system api's payload after you upload files"
    )
    blocked: bool = Field(description="The brand is blocked or not")
    description: str = Field(description="the description of brand, max-length: 1000")
    collection_book_id: Optional[str] = Field(description="the uuid of collection book")
    drops: list = Field(default=[], description="The uuids of drops")


class CreateBrandResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class EditBrandPathParams(FrozenBaseModel):
    id: str = Field(description="the uuid of brand")


class EditBrandParams(FrozenBaseModel):
    name: str = Field(description="the name of brand, max-length: 30")
    slug: str = Field(description="the slug of brand, max-length: 16")
    cover: str = Field(
        description="the cover of brand, a uuid which comes from system api's payload after you upload files"
    )
    blocked: bool = Field(description="The brand is blocked or not")
    description: str = Field(description="the description of brand, max-length: 1000")
    collection_book_id: Optional[str] = Field(description="the uuid of collection book")
    drops: list = Field(default=[], description="The uuids of drops")


class EditBrandResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class GetCollectionBookListParams(FrozenBaseModel):
    current_page: int = Field(description="The page number wanna to get, min: 1")
    page_size: Optional[int] = Field(default=20, description="Number of rows of the page, max: 100")
    name: Optional[str] = Field(description="collection-book name, max-length: 256")


class GetCollectionBookListResponse(RestResponse):
    data: list = Field()
    total: int = Field()


class GetCollectionBookDetailPathParams(FrozenBaseModel):
    id: int = Field(description="uuid of created collection book")


class GetCollectionBookDetailResponse(RestResponse):
    uuid: str = Field(description="The uuid of created collection book")
    name: str = Field(description="The name of created collection book")
    display_name: str = Field(description="The displayName of created collection book")
    cta_name: str = Field(description="The ctaName of created collection book")
    description: str = Field(description="The description of created collection book")
    active: bool = Field(description="The status of created collection book")
    creator_id: str = Field(description="The creatorId of created collection book")
    cover: str = Field(description="collection-book cover image")
    segment: list = Field(description="The array list of binding segments' info")


class CreateCollectionBookParams(FrozenBaseModel):
    name: str = Field(description="collection-book name, max-length: 256")
    display_name: str = Field(description="collection-book display-name, max-length: 256")
    description: str = Field(description="collection-book description, max-length: 2056")
    cta_name: str = Field(description="collection-book CTA name, max-length: 2056")
    creator_id: str = Field(description="collection-book creatorId")
    active: bool = Field(description="collection-book status")
    cover: Optional[str] = Field(description="collection-book cover image")


class CreateCollectionBookResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class EditCollectionBookPathParams(FrozenBaseModel):
    id: str = Field(description="collection-book created uuid")


class EditCollectionBookParams(FrozenBaseModel):
    name: Optional[str] = Field(description="collection-book name, max-length: 256")
    display_name: Optional[str] = Field(description="collection-book display-name, max-length: 256")
    description: Optional[str] = Field(description="collection-book description, max-length: 2056")
    cta_name: Optional[str] = Field(description="collection-book CTA name, max-length: 2056")
    active: Optional[bool] = Field(description="collection-book status")
    cover: Optional[str] = Field(description="collection-book cover image")


class EditCollectionBookResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class AttachSegmentToCollectionBookPathParams(FrozenBaseModel):
    id: str = Field(description="collection-book created uuid")


class AssetConfig(FrozenBaseModel):
    uuid: str = Field(description="uuid of created asset")
    placeholder: str = Field(description="image uuid")


class AttachSegmentToCollectionBookParams(FrozenBaseModel):
    name: str = Field(description="collection-book name, max-length: 256")
    active: bool = Field(description="collection-book status")
    assets: List[AssetConfig] = Field(default=[], description="collection-book asset uuid/placeholder array")
    placeholder: str = Field(description="collection-book placeholder url address")


class AttachSegmentToCollectionBookResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class UpdateAssetPlaceholderPathParams(FrozenBaseModel):
    id: str = Field(description="uuid of created asset")


class UpdateAssetPlaceholderParams(FrozenBaseModel):
    uuid: str = Field(description="image uuid")
    placeholder: str = Field(description="segment uuid")


class UpdateAssetPlaceholderResponse(RestResponse):
    code: int = Field()
    message: str = Field()
