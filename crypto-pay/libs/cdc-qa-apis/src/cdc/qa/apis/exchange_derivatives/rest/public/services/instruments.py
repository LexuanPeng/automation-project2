from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.exchange_derivatives.rest.rest_base import DerivativesRestApi, DerivativesRestService

from ..models.instruments import (
    GetExpiredSettlementPriceParams,
    GetExpiredSettlementPriceResponse,
    GetInstrumentsResponse,
    GetInstrumentsResponseV3,
)


class GetInstrumentsApi(DerivativesRestApi):
    """Provides information on all supported instruments (e.g. BTC_USDT)"""

    path = "public/get-instruments"
    method = HttpMethods.GET
    response_type = GetInstrumentsResponse


class GetInstrumentsApiV3(DerivativesRestApi):
    """Provides information on all supported instruments (e.g. BTC_USDT)"""

    path = "public/get-instruments"
    method = HttpMethods.GET
    response_type = GetInstrumentsResponseV3


class GetBetaInstrumentsApi(DerivativesRestApi):
    """
    Provides information on all supported beta instruments
    """

    path = "public/get-beta-instruments"
    method = HttpMethods.GET
    response_type = GetInstrumentsResponse


class GetExpiredSettlementPriceApi(DerivativesRestApi):
    """
    Fetches settlement price of expired instruments.
    """

    path = "public/get-expired-settlement-price"
    method = HttpMethods.GET
    request_params_type = GetExpiredSettlementPriceParams
    response_type = GetExpiredSettlementPriceResponse


class InstrumentsService(DerivativesRestService):
    def get_instruments(self) -> GetInstrumentsResponse:
        api = GetInstrumentsApi(host=self.host, _session=self.session)
        response = GetInstrumentsResponse.parse_raw(b=api.call().content)
        return response

    def get_instruments_v3(self) -> GetInstrumentsResponseV3:
        api = GetInstrumentsApiV3(host=self.host, _session=self.session)
        response = GetInstrumentsResponseV3.parse_raw(b=api.call().content)
        return response

    def get_beta_instruments(self) -> GetInstrumentsResponse:
        api = GetBetaInstrumentsApi(host=self.host, _session=self.session)
        response = GetInstrumentsResponse.parse_raw(b=api.call().content)
        return response

    def get_expired_settlement_price(self, instrument_type: str, page: int = None) -> GetExpiredSettlementPriceResponse:
        """Fetches settlement price of expired instruments.

        Args:
            instrument_type (str): instrument type. e.g: FUTURE
            page (int, optional): page number. Defaults to None.

        Returns:
            GetExpiredSettlementPriceResponse: GetExpiredSettlementPriceResponse
        """
        api = GetExpiredSettlementPriceApi(host=self.host, _session=self.session)
        params = GetExpiredSettlementPriceParams(instrument_type=instrument_type, page=page).dict(exclude_none=True)
        response = GetExpiredSettlementPriceResponse.parse_raw(b=api.call(params=params).content)

        return response
