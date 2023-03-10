from typing import Optional
from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.rails.models import RailsRestApi, RailsRestService
from cdc.qa.apis.rails.models.crypto_wallets import (
    CryptoWalletsTransactionsQueryParams,
    CryptoWalletsTransactionsResponse,
    CryptoWalletsShowQueryParams,
    CryptoWalletsShowResponse,
)


class CryptoWalletsTransactionsApi(RailsRestApi):
    """Get crypto wallets transactions."""

    path = "crypto_wallets/transactions"
    method = HttpMethods.GET
    request_params_type = CryptoWalletsTransactionsQueryParams
    response_type = CryptoWalletsTransactionsResponse


class CryptoWalletsShowApi(RailsRestApi):
    """Get specific crypto wallet"""

    path = "wallets/show"
    method = HttpMethods.GET
    request_params_type = CryptoWalletsShowQueryParams
    response_type = CryptoWalletsShowResponse


class CryptoWalletsService(RailsRestService):
    def transactions(self, count: int = 1, currency: Optional[str] = None) -> CryptoWalletsTransactionsResponse:
        api = CryptoWalletsTransactionsApi(host=self.host, _session=self.session)
        params = CryptoWalletsTransactionsQueryParams(count=count, currency=currency).dict(exclude_none=True)

        response = api.call(params=params)
        return CryptoWalletsTransactionsResponse.parse_raw(b=response.content)

    def show(self, currency: str) -> CryptoWalletsShowResponse:
        api = CryptoWalletsShowApi(host=self.host, _session=self.session)
        params = CryptoWalletsShowQueryParams(currency=currency).dict(exclude_none=True)

        response = api.call(params=params)
        return CryptoWalletsShowResponse.parse_raw(b=response.content)
