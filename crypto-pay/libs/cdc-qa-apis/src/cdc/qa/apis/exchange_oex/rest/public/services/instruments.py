from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.exchange_oex.rest.rest_base import ExchangeRestApi, ExchangeRestService

from ..models.instruments import (
    GetBetaInstrumentsResponse,
    GetCurrenciesResponse,
    GetDepositInstrumentsResponse,
    GetExpiredSettlementPriceParams,
    GetExpiredSettlementPriceResponse,
    GetInstrumentsResponse,
    GetInstrumentsResponseV3,
    GetInstrumentsV3PathParams,
    GetRiskParametersResponse,
)


class GetInstrumentsApi(ExchangeRestApi):
    """Provides information on all supported instruments (e.g. BTC_USDT)"""

    path = "public/get-instruments"
    method = HttpMethods.GET
    response_type = GetInstrumentsResponse


class GetInstrumentsApiV3(ExchangeRestApi):
    """Provides information on all supported instruments (e.g. BTC_USDT)"""

    path = "public/get-instruments"
    method = HttpMethods.GET
    response_type = GetInstrumentsResponseV3


class GetBetaInstrumentsApi(ExchangeRestApi):
    """
    Provides information on all supported beta instruments
    """

    path = "public/get-beta-instruments"
    method = HttpMethods.GET
    response_type = GetBetaInstrumentsResponse


class GetInstrumentsApiV3InstrumentType(ExchangeRestApi):
    """Provides information on all supported instruments (e.g. BTC_USDT)"""

    @staticmethod
    def path(path_params: GetInstrumentsV3PathParams):
        return f"public/get-instruments/instrument_type/{path_params.instrument_type}"

    method = HttpMethods.GET
    path_params_type = GetInstrumentsV3PathParams
    response_type = GetInstrumentsResponseV3


class GetExpiredSettlementPriceApi(ExchangeRestApi):
    """
    Fetches settlement price of expired instruments.
    """

    path = "public/get-expired-settlement-price"
    method = HttpMethods.GET
    request_params_type = GetExpiredSettlementPriceParams
    response_type = GetExpiredSettlementPriceResponse


class GetDepositInstrumentsApi(ExchangeRestApi):
    path = "public/get-deposit-instruments"
    method = HttpMethods.GET
    response_type = GetDepositInstrumentsResponse


class GetCurrenciesApi(ExchangeRestApi):
    path = "public/get-currencies"
    method = HttpMethods.GET
    response_type = GetCurrenciesResponse


class GetRiskParametersApi(ExchangeRestApi):
    path = "public/get-risk-parameters"
    method = HttpMethods.GET
    response_type = GetRiskParametersResponse


class InstrumentsService(ExchangeRestService):
    def get_instruments(self) -> GetInstrumentsResponse:
        api = GetInstrumentsApi(host=self.host, _session=self.session)
        response = GetInstrumentsResponse.parse_raw(b=api.call().content)
        return response

    def get_instruments_v3(self) -> GetInstrumentsResponseV3:
        api = GetInstrumentsApiV3(host=self.host, _session=self.session)
        response = GetInstrumentsResponseV3.parse_raw(b=api.call().content)
        return response

    def get_instruments_v3_instrument_type(self, instrument_type: str) -> GetInstrumentsResponseV3:
        """request v3/public/get-instruments by instrument_type"""
        api = GetInstrumentsApiV3InstrumentType(host=self.host, _session=self.session)
        path_params = GetInstrumentsV3PathParams(instrument_type=instrument_type)
        response = GetInstrumentsResponseV3.parse_raw(b=api.call(path_params=path_params).content)
        return response

    def get_beta_instruments(self) -> GetBetaInstrumentsResponse:
        api = GetBetaInstrumentsApi(host=self.host, _session=self.session)
        response = GetBetaInstrumentsResponse.parse_raw(b=api.call().content)
        return response

    def get_expired_settlement_price(self, instrument_type: str, page: int = None) -> GetExpiredSettlementPriceResponse:
        """Fetches settlement price of expired instruments.

        Args:
            instrument_type (str): instrument type. e.g: FUTURE
            page (int, optional): page number. Defaults to 1.

        Returns:
            GetExpiredSettlementPriceResponse: GetExpiredSettlementPriceResponse
        """
        api = GetExpiredSettlementPriceApi(host=self.host, _session=self.session)
        params = GetExpiredSettlementPriceParams(instrument_type=instrument_type, page=page).dict(exclude_none=True)
        response = GetExpiredSettlementPriceResponse.parse_raw(b=api.call(params=params).content)

        return response

    def get_deposit_instruments(self) -> GetDepositInstrumentsResponse:
        api = GetDepositInstrumentsApi(host=self.host, _session=self.session)
        response = GetDepositInstrumentsResponse.parse_raw(b=api.call().content)
        return response

    def get_currencies(self) -> GetCurrenciesResponse:
        api = GetCurrenciesApi(host=self.host, _session=self.session)
        response = GetCurrenciesResponse.parse_raw(b=api.call().content)
        return response

    def get_risk_parameters(self) -> GetRiskParametersResponse:
        api = GetRiskParametersApi(host=self.host, _session=self.session)
        response = GetRiskParametersResponse.parse_raw(b=api.call().content)
        return response
