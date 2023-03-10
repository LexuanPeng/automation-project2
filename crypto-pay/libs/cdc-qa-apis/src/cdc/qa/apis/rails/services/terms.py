import logging

from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.rails.models import RailsRestService, RailsRestApi
from cdc.qa.apis.rails.models.terms import (
    TermsMandatoryTermsPendingResponse,
    TermsMandatoryTermsAcceptRequestData,
    TermsMandatoryTermsAcceptResponse,
)

logger = logging.getLogger(__name__)


class TermsMandatoryTermsPendingApi(RailsRestApi):
    """Get list of mandatory terms pending to be accept."""

    path = "terms/mandatory_terms/pending"
    method = HttpMethods.GET
    response_type = TermsMandatoryTermsPendingResponse


class TermsMandatoryTermsAcceptApi(RailsRestApi):
    """Accept Terms and Conditions when the user first enter Home screen."""

    path = "terms/mandatory_terms/accept"
    method = HttpMethods.POST
    request_data_type = TermsMandatoryTermsAcceptRequestData
    response_type = TermsMandatoryTermsAcceptResponse


class TermsService(RailsRestService):
    def _mandatory_terms_pending(self) -> TermsMandatoryTermsPendingResponse:
        api = TermsMandatoryTermsPendingApi(host=self.host, _session=self.session)

        response = api.call()
        return TermsMandatoryTermsPendingResponse.parse_raw(b=response.content)

    def _mandatory_terms_accept(self, terms_id: str) -> TermsMandatoryTermsAcceptResponse:
        api = TermsMandatoryTermsAcceptApi(host=self.host, _session=self.session)
        data = TermsMandatoryTermsAcceptRequestData(id=terms_id).dict(exclude_none=True)

        response = api.call(data=data)
        return TermsMandatoryTermsAcceptResponse.parse_raw(b=response.content)

    def accept_terms(self):
        for terms in self._mandatory_terms_pending().mandatory_terms:
            self._mandatory_terms_accept(terms.id)
            logger.debug(f"Terms {terms.name} accepted")
