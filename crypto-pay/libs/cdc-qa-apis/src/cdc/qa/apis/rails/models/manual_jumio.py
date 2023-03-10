from typing import Optional

from cdc.qa.apis.rails.data.jumio import DocumentType
from cdc.qa.apis.rails.models import FrozenBaseModel, RailsResponse

from pydantic import Field, validator
from urllib.parse import urlparse, parse_qs


# ManualJumioCreate
class ManualJumioCreateRequestData(FrozenBaseModel):
    country_code: str = Field()
    document_type: DocumentType = Field()

    class Config:
        use_enum_values = True


class ManualJumioCreateResponse(RailsResponse):
    class ManualJumio(FrozenBaseModel):
        status: str = Field()

    manual_jumio: ManualJumio = Field()


# ManualJumioNew
class ManualJumioNewRequestParams(FrozenBaseModel):
    country_code: str = Field()


class UploadUrl(FrozenBaseModel):
    host: str = Field()
    path: str = Field()
    query_params: dict = Field()


class UploadUrls(FrozenBaseModel):

    liveness: UploadUrl = Field()
    selfie: UploadUrl = Field()
    id_card_front: UploadUrl = Field()
    id_card_back: UploadUrl = Field()
    driver_license_front: Optional[UploadUrl] = Field()
    driver_license_back: Optional[UploadUrl] = Field()
    passport: Optional[UploadUrl] = Field()

    @validator("*", pre=True)
    def split_url(cls, v):
        if isinstance(v, str):
            result = urlparse(v)
            return UploadUrl(
                host=f"{result.scheme}://{result.netloc}",
                path=result.path,
                query_params={k: v[0] for k, v in parse_qs(result.query).items()},
            )
        return v


class ManualJumioNewResponse(RailsResponse):

    upload_urls: UploadUrls = Field()
    handwritten: str = Field()
