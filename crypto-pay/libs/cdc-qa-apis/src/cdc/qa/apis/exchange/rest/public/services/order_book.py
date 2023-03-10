from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.exchange.rest.rest_base import ExchangeRestApi, ExchangeRestService

from ..models.order_book import GetBookRequestParams, GetBookResponse


class GetBookApi(ExchangeRestApi):
    """exchange-public get order book"""

    path = "public/get-book"
    method = HttpMethods.GET
    request_params_type = GetBookRequestParams
    response_type = GetBookResponse


class BookService(ExchangeRestService):
    def get_book(self, instrument_name: str, depth: int = None) -> GetBookResponse:
        api = GetBookApi(host=self.host, _session=self.session)
        params = GetBookRequestParams(instrument_name=instrument_name, depth=depth).dict(exclude_none=True)
        response = GetBookResponse.parse_raw(b=api.call(params=params).content)

        return response
