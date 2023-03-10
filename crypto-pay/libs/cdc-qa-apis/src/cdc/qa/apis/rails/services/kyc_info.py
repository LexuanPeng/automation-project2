from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.rails.models import RailsRestApi, RailsRestService
from cdc.qa.apis.rails.models.kyc_info import (
    KYCInfoSubmitAdditionalCollectionQuestionResponse,
    KYCInfoSubmitAdditionalCollectionQuestionRequestData,
    KYCInfoAdditionalCollectionQuestionResponse,
    KYCInfoAdditionalCollectionOverviewQueryParams,
    KYCInfoAdditionalCollectionQuestionQueryParams,
    KYCInfoAdditionalCollectionOverviewResponse,
    FieldAnswer,
)


class KYCInfoAdditionalCollectionOverviewApi(RailsRestApi):
    """Overview KYC Info Additional Collection"""

    path = "kyc_info/additional_collection/overview"
    method = HttpMethods.GET
    request_params_type = KYCInfoAdditionalCollectionOverviewQueryParams
    response_type = KYCInfoAdditionalCollectionOverviewResponse


class KYCInfoAdditionalCollectionQuestionApi(RailsRestApi):
    """Get KYC Info Additional Collection Questions"""

    path = "kyc_info/additional_collection/question"
    method = HttpMethods.GET
    request_params_type = KYCInfoAdditionalCollectionQuestionQueryParams
    response_type = KYCInfoAdditionalCollectionQuestionResponse


class KYCInfoSubmitAdditionalCollectionQuestionApi(RailsRestApi):
    """Submit Answers for KYC Info Additional Collection Questions"""

    path = "kyc_info/additional_collection/question"
    method = HttpMethods.POST
    request_data_type = KYCInfoSubmitAdditionalCollectionQuestionRequestData
    response_type = KYCInfoSubmitAdditionalCollectionQuestionResponse


class KYCInfoService(RailsRestService):
    def overview_kyc_additional_info(self, triggered_by: str) -> KYCInfoAdditionalCollectionOverviewResponse:
        api = KYCInfoAdditionalCollectionOverviewApi(host=self.host, _session=self.session)
        params = KYCInfoAdditionalCollectionOverviewQueryParams(triggered_by=triggered_by).dict(exclude_none=True)

        response = api.call(params=params)
        return KYCInfoAdditionalCollectionOverviewResponse.parse_raw(b=response.content)

    def get_kyc_additional_info_questions(
        self,
        section_id: str,
        triggered_by: str,
    ) -> KYCInfoAdditionalCollectionQuestionResponse:
        api = KYCInfoAdditionalCollectionQuestionApi(host=self.host, _session=self.session)
        params = KYCInfoAdditionalCollectionQuestionQueryParams(section_id=section_id, triggered_by=triggered_by).dict(
            exclude_none=True
        )

        response = api.call(params=params)
        return KYCInfoAdditionalCollectionQuestionResponse.parse_raw(b=response.content)

    def submit_kyc_additional_info(
        self, request_data: KYCInfoSubmitAdditionalCollectionQuestionRequestData
    ) -> KYCInfoSubmitAdditionalCollectionQuestionResponse:
        api = KYCInfoSubmitAdditionalCollectionQuestionApi(host=self.host, _session=self.session)

        data = request_data.dict(exclude_none=True)

        response = api.call(json=data)
        return KYCInfoSubmitAdditionalCollectionQuestionResponse.parse_raw(b=response.content)

    def submit_turkey_user_residential_address(self):
        """
        Hardcoded turkey user's data will be submitted
        """

        triggered_by = "account_creation"
        """
        Get KYC account_creation items
        The items are: residential_address, nationality, parents_name, occupation, purpose_of_account
        """
        account_creation_overview = self.overview_kyc_additional_info(triggered_by=triggered_by).overview
        for overview in account_creation_overview:
            questions_data = self.get_kyc_additional_info_questions(
                triggered_by=triggered_by, section_id=overview.section_id
            )

            if questions_data.section_id == "residential_address":
                """
                Answering residential_address questions
                """
                answers = []
                for field in questions_data.fields:
                    """
                    Generating Address Data
                    """
                    if field.name == "address":
                        address = KYCInfoSubmitAdditionalCollectionQuestionRequestData.Answer(
                            question_id=field.question_id, field_name=field.name, field_answer="address"
                        )
                        answers.append(address)
                    elif field.name == "city":
                        field_answers = [FieldAnswer(id="1", value="ADANA", is_other=False)]
                        city = KYCInfoSubmitAdditionalCollectionQuestionRequestData.Answer(
                            question_id=field.question_id, field_name=field.name, field_answers=field_answers
                        )
                        answers.append(city)
                    elif field.name == "zip_code":
                        zip_code = KYCInfoSubmitAdditionalCollectionQuestionRequestData.Answer(
                            question_id=field.question_id, field_name=field.name, field_answer="44444"
                        )
                        answers.append(zip_code)
                    elif field.name == "attest_address":
                        attest_address = KYCInfoSubmitAdditionalCollectionQuestionRequestData.Answer(
                            question_id=field.question_id, field_name=field.name, field_answer="true"
                        )
                        answers.append(attest_address)
                    elif field.name == "town":
                        field_answers = [FieldAnswer(id="4", value="FEKE", is_other=False)]
                        town = KYCInfoSubmitAdditionalCollectionQuestionRequestData.Answer(
                            question_id=field.question_id, field_name=field.name, field_answers=field_answers
                        )
                        answers.append(town)
                    elif field.name == "neighborhood":
                        field_answers = [FieldAnswer(id="172", value="AKKAYA MAH", is_other=False)]
                        neighborhood = KYCInfoSubmitAdditionalCollectionQuestionRequestData.Answer(
                            question_id=field.question_id, field_name=field.name, field_answers=field_answers
                        )
                        answers.append(neighborhood)
                    elif field.input_type == "read_only":
                        # Read only field is not required to fill in
                        pass
                    else:
                        raise ValueError(f"New question appeared: {field.name}")

                residential_address_data = KYCInfoSubmitAdditionalCollectionQuestionRequestData(
                    triggered_by=triggered_by, answers=answers
                )
                self.submit_kyc_additional_info(request_data=residential_address_data)

            elif questions_data.section_id == "nationality":
                """
                Answering nationality questions
                """
                answers = []
                for field in questions_data.fields:
                    """
                    Generating Nationality Data
                    """
                    if field.name == "nationality":
                        field_answers = [
                            FieldAnswer(
                                id="211", value="Turkish", translation_key="country_full_name__tur", is_other=False
                            )
                        ]
                        nationality = KYCInfoSubmitAdditionalCollectionQuestionRequestData.Answer(
                            question_id=field.question_id, field_name=field.name, field_answers=field_answers
                        )
                        answers.append(nationality)
                    elif field.name == "place_of_birth":
                        field_answers = [FieldAnswer(id="1", value="ADANA", is_other=False)]
                        nationality = KYCInfoSubmitAdditionalCollectionQuestionRequestData.Answer(
                            question_id=field.question_id, field_name=field.name, field_answers=field_answers
                        )
                        answers.append(nationality)
                    elif field.input_type == "read_only":
                        # Read only field is not required to fill in
                        pass
                    else:
                        raise ValueError(f"New question appeared: {field.name}")
                nationality_data = KYCInfoSubmitAdditionalCollectionQuestionRequestData(
                    triggered_by=triggered_by, answers=answers
                )
                self.submit_kyc_additional_info(request_data=nationality_data)

            elif questions_data.section_id == "parents_name":
                """
                Answering parents_name questions
                """
                answers = []
                for field in questions_data.fields:
                    """
                    Generating parents_name Data
                    """
                    if field.name == "father_name":
                        father_name = KYCInfoSubmitAdditionalCollectionQuestionRequestData.Answer(
                            question_id=field.question_id, field_name=field.name, field_answer="father"
                        )
                        answers.append(father_name)
                    elif field.name == "mother_name":
                        mother_name = KYCInfoSubmitAdditionalCollectionQuestionRequestData.Answer(
                            question_id=field.question_id, field_name=field.name, field_answer="mother"
                        )
                        answers.append(mother_name)
                    elif field.input_type == "read_only":
                        # Read only field is not required to fill in
                        pass
                    else:
                        raise ValueError(f"New question appeared: {field.name}")

                parents_name_data = KYCInfoSubmitAdditionalCollectionQuestionRequestData(
                    triggered_by=triggered_by, answers=answers
                )
                self.submit_kyc_additional_info(request_data=parents_name_data)

            elif questions_data.section_id == "occupation":
                """
                Answering occupation questions
                """
                answers = []
                for field in questions_data.fields:
                    """
                    Generating occupation Data
                    """
                    if field.name == "occupation":
                        field_answers = [
                            FieldAnswer(
                                id="1",
                                value="clergy",
                                translation_key="cad_fiat_identity_verification_occupation_list_selected",
                                is_other=False,
                            )
                        ]
                        occupation = KYCInfoSubmitAdditionalCollectionQuestionRequestData.Answer(
                            question_id=field.question_id, field_name=field.name, field_answers=field_answers
                        )
                        answers.append(occupation)
                    elif field.input_type == "read_only":
                        # Read only field is not required to fill in
                        pass
                    else:
                        raise ValueError(f"New question appeared: {field.name}")

                occupation_data = KYCInfoSubmitAdditionalCollectionQuestionRequestData(
                    triggered_by=triggered_by, answers=answers
                )
                self.submit_kyc_additional_info(request_data=occupation_data)

            elif questions_data.section_id == "purpose_of_account":
                """
                Answering purpose_of_account questions
                """
                answers = []
                for field in questions_data.fields:
                    """
                    Generating purpose_of_account Data
                    """
                    if field.name == "purpose_of_account":
                        field_answers = [
                            FieldAnswer(
                                id="1",
                                value="trading",
                                translation_key="kyc_label_purpose_selection_trading",
                                is_other=False,
                            )
                        ]
                        purpose_of_account = KYCInfoSubmitAdditionalCollectionQuestionRequestData.Answer(
                            question_id=field.question_id, field_name=field.name, field_answers=field_answers
                        )
                        answers.append(purpose_of_account)
                    elif field.input_type == "read_only":
                        # Read only field is not required to fill in
                        pass
                    else:
                        raise ValueError(f"New question appeared: {field.name}")

                purpose_of_account_data = KYCInfoSubmitAdditionalCollectionQuestionRequestData(
                    triggered_by=triggered_by, answers=answers
                )
                self.submit_kyc_additional_info(request_data=purpose_of_account_data)

            else:
                raise ValueError(f"New section_id appeared: {questions_data.section_id}")
