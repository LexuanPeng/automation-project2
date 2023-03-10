from typing import Optional

from pydantic import Field

from cdc.qa.apis.crypto_nft_admin.models import RestResponse, FrozenBaseModel


class GetCategoryListParams(FrozenBaseModel):
    current_page: int = Field(description="The page number wanna to get, min: 1")
    page_size: Optional[int] = Field(default=20, description="Number of rows of the page, max: 100")
    name: Optional[str] = Field(description="category name, max-length: 256")


class GetCategoryListResponse(RestResponse):
    data: list = Field()
    total: int = Field()


class GetCategoryListAbnormalResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class GetCategoryListShowStatusParams(FrozenBaseModel):
    current_page: int = Field(description="The page number wanna to get, min: 1")
    page_size: Optional[int] = Field(default=20, description="Number of rows of the page, max: 100")
    name: Optional[str] = Field(description="category name, max-length: 256")


class GetCategoryListShowStatusResponse(RestResponse):
    data: list = Field()
    total: int = Field()


class GetCategoryListShowStatusAbnormalResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class CreateCategoryParams(FrozenBaseModel):
    name: str = Field(description="category name, max-length: 256")


class CreateCategoryResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class EditCategoryPathParams(FrozenBaseModel):
    id: str = Field(description="category uuid")


class EditCategoryParams(FrozenBaseModel):
    name: str = Field(description="category name, max-length: 256")


class EditCategoryResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class CreateCategoryDWParams(FrozenBaseModel):
    name: str = Field(description="category name, max-length: 256")


class CreateCategoryDWResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class EditCategoryDWPathParams(FrozenBaseModel):
    id: str = Field(description="category uuid")


class EditCategoryDWParams(FrozenBaseModel):
    name: str = Field(description="category name, max-length: 256")


class EditCategoryDWResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class UpdateCategoryStatusPathParams(FrozenBaseModel):
    id: str = Field(description="category uuid")


class UpdateCategoryStatusParams(FrozenBaseModel):
    show: bool = Field(description="category's show status")


class UpdateCategoryStatusResponse(RestResponse):
    code: int = Field()
    message: str = Field()


class UpdateCategoryStatusDWPathParams(FrozenBaseModel):
    id: str = Field(description="category uuid")


class UpdateCategoryStatusDWParams(FrozenBaseModel):
    show: bool = Field(description="category's show status")


class UpdateCategoryStatusDWResponse(RestResponse):
    code: int = Field()
    message: str = Field()
