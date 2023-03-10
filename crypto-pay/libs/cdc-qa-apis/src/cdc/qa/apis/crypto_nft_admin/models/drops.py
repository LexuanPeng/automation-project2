from typing import Optional, Any

from pydantic import Field

from cdc.qa.apis.crypto_nft_admin.models import RestResponse, FrozenBaseModel


class GetDropsDetailParams(FrozenBaseModel):
    current_page: int = Field(description="The page number wanna to get, min: 1")
    page_size: Optional[int] = Field(default=20, description="Number of rows of the page, max: 100")
    id: Optional[str] = Field(description="the id of drop")
    name: Optional[str] = Field(description="the name of drop, max-length: 256")
    creator_uuids: Optional[list] = Field(default=[], description="the matching creators uuid list")


class GetDropsResponse(RestResponse):
    data: list = Field()
    total: int = Field()


class GetDropsAbnormalResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class GetDropsByUuidPathParams(FrozenBaseModel):
    uuid: str = Field(description="the uuid of drop")


class GetDropsByUuidResponse(RestResponse):
    auction_max_end_date: Optional[Any] = Field(description="The auctionMaxEndDate of created drop-asset")
    blocked: bool = Field(description="The blocked of created drop-asset")
    category_list: Any = Field(description="The category list of created drop-asset")
    collection: Optional[Any] = Field(description="The collection of drop-asset")
    cover: Any = Field(description="The cover of created drop-asset")
    creator_info: Any = Field(description="The creator of drop-asset")
    main: Any = Field(description="The main of created drop-asset")
    properties: Optional[list] = Field(description="The category list of created drop-asset")
    price: Optional[int] = Field(description="The price of asset")
    drop_name: Optional[str] = Field(description="The drop name")
    sale_mode: Optional[int] = Field(description="the sale mode of drop-asset")
    showcopiesincirculation: Optional[bool] = Field(
        description="The showcopiesincirculation status of created drop-asset"
    )
    status: Optional[int] = Field(description="The status of created drop-asset")
    type: Optional[int] = Field(description="The type of created drop-asset")
    description: Optional[str] = Field(description="The description of created drop-asset")
    id: int = Field(description="The id of drop-asset")
    editions: Optional[int] = Field(description="The editions of created drop-asset")
    on_chain: Optional[bool] = Field(description="The onChain status of created drop-asset")
    name: str = Field(description="The drop name")
    remark: Optional[str] = Field(description="The remark of created drop-asset")
    royalty: Optional[int] = Field(description="The royalty of created drop-asset")
    uuid: str = Field(description="The uuid of created drop-asset")
    withdrawal: Optional[bool] = Field(description="The withdrawal of created drop-asset")


class GetDropsByUuidAbnormalResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class CreateDropsDetailParams(FrozenBaseModel):
    name: str = Field(description="the name of drop, max-length: 256")
    description: str = Field(description="the what's inside description field of drop")
    creator_info: str = Field(description="the creator info field of drop")
    start_time: str = Field(
        description="the start time of drop, must after current time, eg.: 2022-12-12T18:30:30.222Z"
    )
    end_time: str = Field(
        description="the end time of drop, must after start time and current time, eg.: 2022-12-12T18:30:30.222Z"
    )
    creator_id: str = Field(description="the creatorId of drop")
    show_collectible: bool = Field(default=True, description="showCollectible of drop's creation")
    public_read_only: bool = Field(default=False, description="publicReadOnly of drop's creation")
    cover: Optional[str] = Field(
        description="the cover of drop, a uuid which comes from system api's payload after you upload files"
    )
    video: Optional[str] = Field(
        description="the video of drop, a uuid which comes from system api's payload after you upload files"
    )
    terms_and_conditions: Optional[str] = Field(description="the terms and conditions field of drop")
    what_inside_description: Optional[str] = Field(description="the what's inside description field of drop")


class CreateDropsResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class EditDropsPathParams(FrozenBaseModel):
    id: str = Field(description="the generated id of drop")


class EditDropsDetailParams(FrozenBaseModel):
    name: str = Field(description="the name of drop, max-length: 256")
    description: str = Field(description="the what's inside description field of drop")
    creator_info: str = Field(description="the creator info field of drop")
    start_time: str = Field(
        description="the start time of drop, must after current time, eg.: 2022-12-12T18:30:30.222Z"
    )
    end_time: str = Field(
        description="the end time of drop, must after start time and current time, eg.: 2022-12-12T18:30:30.222Z"
    )
    blocked: bool = Field(description="the drop is blocked or not")
    show_collectible: bool = Field(default=True, description="showCollectible of drop's creation")
    public_read_only: bool = Field(default=False, description="publicReadOnly of drop's creation")
    cover: Optional[str] = Field(
        description="the cover of drop, a uuid which comes from system api's payload after you upload files"
    )
    video: Optional[str] = Field(
        description="the video of drop, a uuid which comes from system api's payload after you upload files"
    )
    terms_and_conditions: Optional[str] = Field(description="the terms and conditions field of drop")
    what_inside_description: Optional[str] = Field(description="the what's inside description field of drop")


class EditDropsResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class CreateDropsDwDetailParams(FrozenBaseModel):
    name: str = Field(description="the name of drop, max-length: 256")
    description: str = Field(description="the what's inside description field of drop")
    creator_info: str = Field(description="the creator info field of drop")
    start_time: str = Field(
        description="the start time of drop, must after current time, eg.: 2022-12-12T18:30:30.222Z"
    )
    end_time: str = Field(
        description="the end time of drop, must after start time and current time, eg.: 2022-12-12T18:30:30.222Z"
    )
    creator_id: str = Field(description="the creatorId of drop")
    show_collectible: bool = Field(default=True, description="showCollectible of drop's creation")
    public_read_only: bool = Field(default=False, description="publicReadOnly of drop's creation")
    cover: Optional[str] = Field(
        description="the cover of drop, a uuid which comes from system api's payload after you upload files"
    )
    video: Optional[str] = Field(
        description="the video of drop, a uuid which comes from system api's payload after you upload files"
    )
    terms_and_conditions: Optional[str] = Field(description="the terms and conditions field of drop")
    what_inside_description: Optional[str] = Field(description="the what's inside description field of drop")


class CreateDropsDwResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class EditDropsDwPathParams(FrozenBaseModel):
    id: str = Field(description="the generated id of drop")


class EditDropsDwDetailParams(FrozenBaseModel):
    name: str = Field(description="the name of drop, max-length: 256")
    description: str = Field(description="the what's inside description field of drop")
    creator_info: str = Field(description="the creator info field of drop")
    start_time: str = Field(
        description="the start time of drop, must after current time, eg.: 2022-12-12T18:30:30.222Z"
    )
    end_time: str = Field(
        description="the end time of drop, must after start time and current time, eg.: 2022-12-12T18:30:30.222Z"
    )
    blocked: bool = Field(description="the drop is blocked or not")
    show_collectible: bool = Field(default=True, description="showCollectible of drop's creation")
    public_read_only: bool = Field(default=False, description="publicReadOnly of drop's creation")
    cover: Optional[str] = Field(
        description="the cover of drop, a uuid which comes from system api's payload after you upload files"
    )
    video: Optional[str] = Field(
        description="the video of drop, a uuid which comes from system api's payload after you upload files"
    )
    terms_and_conditions: Optional[str] = Field(description="the terms and conditions field of drop")
    what_inside_description: Optional[str] = Field(description="the what's inside description field of drop")


class EditDropsDwResponse(RestResponse):
    code: int = Field()
    message: str = Field()
