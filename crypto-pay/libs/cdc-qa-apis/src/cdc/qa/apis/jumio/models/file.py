from typing import Union

from cdc.qa.apis.jumio.models import FrozenBaseModel
from pydantic import Field


class FileUploadRequestPathParams(FrozenBaseModel):
    upload_url_path: str = Field()


class FileUploadRequestQueryParams(FrozenBaseModel):
    x_amz_expires: int = Field(alias="X-Amz-Expires")
    x_amz_date: str = Field(alias="X-Amz-Date")
    x_amz_algorithm: str = Field(alias="X-Amz-Algorithm")
    x_amz_credential: str = Field(alias="X-Amz-Credential")
    x_amz_signedheaders: str = Field(alias="X-Amz-SignedHeaders")
    x_amz_signature: str = Field(alias="X-Amz-Signature")
    x_amz_security_token: Union[str, None] = Field(alias="X-Amz-Security-Token")
