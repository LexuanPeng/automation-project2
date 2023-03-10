import pytest
from cdc.qa.helpers.database_helper import ExchangeTexdbHelper


@pytest.fixture
def exchange_texdb_helper():
    db_helper = ExchangeTexdbHelper(ExchangeTexdbHelper.ENV.XDEV4)
    yield db_helper


@pytest.mark.slow
def test_get_margin_loan(exchange_texdb_helper):
    result = exchange_texdb_helper.get_margin_loan_config_by_symbol_stake_amount("BTC", 10000)
    assert result


@pytest.mark.slow
def test_domain_user(exchange_texdb_helper):
    result = exchange_texdb_helper.get_domain_user_info_by_email("evelyn.wang+sz13@crypto.com")
    assert result


# @pytest.fixture()
# def exchange_mysqldb_helper():
#     db_helper = ExchangeMysqlHelper(ExchangeMysqlHelper.ENV.XSTA)
#     yield db_helper
#
#
# def test_select_user(exchange_mysqldb_helper):
#     result = exchange_mysqldb_helper.execute_sql("select * from user where email = 'evelyn.wang+sz13@crypto.com'")
#     assert result
