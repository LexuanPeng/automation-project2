from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.qa_tools.services import QAToolRestApi, QAToolRestService

from ..models.exchange import APITransferRequestParams, APITransferResponse, APITransferRequest


class APITransferApi(QAToolRestApi):
    path = "tools/v1/exchange/api_transfer/"
    method = HttpMethods.POST
    request_data_type = APITransferRequestParams
    response_type = APITransferResponse


class ExchangeService(QAToolRestService):
    def api_transfer(
        self, env: str, by_type: str, transfer_type: str, value: str, currencys: list, amount: str
    ) -> APITransferResponse:
        api = APITransferApi(host=self.host, _session=self.session)
        payload = APITransferRequest(
            params=APITransferRequestParams(
                env=env, type=by_type, transfer_type=transfer_type, value=value, currencys=currencys, amount=amount
            ),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)

        response = api.call(data=payload)
        return APITransferResponse.parse_raw(b=response.content)
