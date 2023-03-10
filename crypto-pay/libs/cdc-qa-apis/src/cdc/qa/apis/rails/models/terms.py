from datetime import datetime
from typing import Optional, List

from cdc.qa.apis.rails import RailsResponse
from cdc.qa.apis.rails.models import FrozenBaseModel
from pydantic import HttpUrl, Field


class Document(FrozenBaseModel):
    name: str
    clickable_text_translation_key: str
    url: HttpUrl


class DocumentGroup(FrozenBaseModel):
    group: int
    checkbox_text_translation_key: str
    documents: List[Document]


class MandatoryTerms(FrozenBaseModel):
    id: str
    name: str
    privacy_policy_url: HttpUrl
    terms_url: HttpUrl
    content_title: str
    content_body: str
    accepted: bool
    accepted_at: Optional[datetime]
    document_groups: Optional[List[DocumentGroup]]


# TermsMandatoryTermsPending
class TermsMandatoryTermsPendingResponse(RailsResponse):
    mandatory_terms: List[MandatoryTerms] = Field()


# TermsMandatoryTermsAccept
class TermsMandatoryTermsAcceptRequestData(FrozenBaseModel):
    id: str = Field()


class TermsMandatoryTermsAcceptResponse(RailsResponse):
    mandatory_terms: MandatoryTerms = Field()
