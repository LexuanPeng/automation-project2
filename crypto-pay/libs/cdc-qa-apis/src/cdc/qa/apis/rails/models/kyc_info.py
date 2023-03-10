from typing import Optional, List
from cdc.qa.apis.rails import RailsResponse
from cdc.qa.apis.rails.models import FrozenBaseModel

from pydantic import Field

# --------------------------------- Common used --------------------------------- #


class FieldAnswer(FrozenBaseModel):
    id: str
    value: str
    translation_key: Optional[str]
    is_other: Optional[bool]
    user_input: Optional[str]


# --------------------------------- Overview KYC additional collection --------------------------------- #


class KYCInfoAdditionalCollectionOverviewQueryParams(FrozenBaseModel):
    triggered_by: str


class KYCInfoAdditionalCollectionOverviewResponse(RailsResponse):
    class Overview(FrozenBaseModel):
        section_id: str
        action: str
        status: str

    option_base_url: str
    intro: Optional[str]
    overview: List[Overview]


# --------------------------------- Get KYC additional collection question status ---------------------------- #


class KYCInfoAdditionalCollectionQuestionQueryParams(FrozenBaseModel):
    triggered_by: str
    section_id: str


class KYCInfoAdditionalCollectionQuestionResponse(RailsResponse):
    class Fields(FrozenBaseModel):
        question_id: str
        component: str
        name: str
        input_type: str
        field_title_translation_key: Optional[str]
        field_description_translation_key: Optional[str]
        field_placeholder_translation_key: Optional[str]
        required: bool
        regex: Optional[str]
        regex_error_translation_key: Optional[str]
        max_select: Optional[int]
        searchbar_enabled: Optional[bool]
        options_key: Optional[str]
        prerequisite: Optional[str]
        options: Optional[List[FieldAnswer]]

    section_id: str = Field()
    section_title_translation_key: Optional[str] = Field()
    section_description_translation_key: Optional[str] = Field()
    fields: List[Fields] = Field()


# --------------------------------- Submit KYC additional collection question --------------------------------- #


class KYCInfoSubmitAdditionalCollectionQuestionRequestData(FrozenBaseModel):
    class Answer(FrozenBaseModel):
        question_id: str
        field_name: str
        field_answer: Optional[str]
        field_answers: Optional[List[FieldAnswer]]

    triggered_by: str = Field()
    answers: List[Answer] = Field()


class KYCInfoSubmitAdditionalCollectionQuestionResponse(RailsResponse):
    result_page: Optional[str] = Field()
