from typing import Optional

from pydantic import Field

from cdc.qa.apis.crypto_nft_admin.models import RestResponse, FrozenBaseModel


class CreateCollectionDetailParams(FrozenBaseModel):
    name: str = Field(description="The name of collection, max-length: 256")
    logo: str = Field(description="The logo resource uuid of collection")
    banner: str = Field(description="The banner resource uuid of collection")
    category: list = Field(default=[], description="The uuids of collection's categories")
    description: str = Field(description="The description of collection, max-length: 256")
    creator_id: str = Field(description="The creatorId of collection")


class CreateCollectionResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class EditCollectionPathParams(FrozenBaseModel):
    id: str = Field(description="The uuid of collection")


class EditCollectionDetailParams(FrozenBaseModel):
    name: Optional[str] = Field(description="The name of collection, max-length: 256")
    logo: Optional[str] = Field(description="The logo resource uuid of collection")
    banner: Optional[str] = Field(description="The banner resource uuid of collection")
    category: list = Field(default=[], description="The uuids of collection's categories")
    description: str = Field(description="The description of collection, max-length: 256")


class EditCollectionResponse(RestResponse):
    code: int = Field()
    message: str = Field()
