from pytest import fixture
from cdc.qa.apis.exchange_fe import FeExchangeService


@fixture(scope="session")
def service():
    rest_service = FeExchangeService(host="https://xdev4-www.3ona.co/fe-ex-api/", exchange_token="logintoken")
    yield rest_service
