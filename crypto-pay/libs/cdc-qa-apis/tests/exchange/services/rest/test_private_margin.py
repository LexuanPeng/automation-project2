from cdc.qa.apis import exchange
from .mocks import *  # noqa
from decimal import Decimal
import pytest


@pytest.fixture
def margin_service():
    service = exchange.rest.private.MarginService(api_key="", secret_key="", host="https://uat-api.3ona.co/v2/")
    return service


def test_margin_get_user_config(mock_margin_get_user_config, margin_service):
    response = margin_service.get_user_config()
    assert response.result.stake_amount == 50000000
    currency_config = response.result.currency_configs[0]
    assert currency_config.currency == "ENJ"
    assert currency_config.hourly_rate == Decimal("0.00000417")
    assert currency_config.max_borrow_limit == 2000000
    assert currency_config.min_borrow_limit == 100


def test_margin_get_account_summary(mock_margin_get_account_summary, margin_service):
    response = margin_service.get_account_summary()
    result = response.result
    account = result.accounts[0]
    assert account.balance == Decimal("200.0022")
    assert account.borrowed == Decimal("0.00019372")
    assert account.position == Decimal("200.00200628")
    assert account.positionHomeCurrency == Decimal("4691247.05930368")
    assert account.positionBtc == Decimal("200.00200628")
    assert account.lastPriceHomeCurrency == Decimal("23456")
    assert account.lastPriceBtc == 1
    assert account.currency == "BTC"
    assert account.accrued_interest == 0
    assert account.liquidation_price == 0
    assert not result.is_liquidating
    assert result.total_balance == Decimal("4692748.437311466")
    assert result.total_balance_btc == Decimal("200.06601455")
    assert result.equity_value == Decimal("4692743.893415146")
    assert result.equity_value_btc == Decimal("200.06582083")
    assert result.total_borrowed == Decimal("4.54389632")
    assert result.total_borrowed_btc == Decimal("0.00019372")
    assert result.total_accrued_interest == 0
    assert result.total_accrued_interest_btc == 0
    assert result.margin_ratio == Decimal("1032758.69")
    assert result.margin_score == "GOOD"
    assert result.currency == "USDT"


def test_margin_transfer(mock_margin_transfer, margin_service):
    response = margin_service.transfer(currency="BTC", from_side="SPOT", to="MARGIN", amount=100)
    assert response.code == 0


def test_margin_borrow(mock_margin_borrow, margin_service):
    response = margin_service.borrow(currency="BTC", amount=2)
    assert response.code == 0


def test_margin_repay(mock_margin_repay, margin_service):
    response = margin_service.repay(currency="BTC", amount=2)
    assert response.code == 0


def test_margin_get_transfer_history(mock_margin_get_transfer_history, margin_service):
    response = margin_service.get_transfer_history(direction="IN")
    transfer_info = response.result.transfer_list[0]
    assert transfer_info.direction == "IN"
    assert transfer_info.time == 1627527955482
    assert transfer_info.amount == 100
    assert transfer_info.status == "COMPLETED"


def test_margin_get_borrow_history(mock_margin_get_borrow_history, margin_service):
    response = margin_service.get_borrow_history()
    borrow_info = response.result.borrow_list[0]
    assert borrow_info.loan_id == "1667358632666702944"
    assert borrow_info.currency == "BTC"
    assert borrow_info.loan_amount == 2
    assert borrow_info.borrow_time == 1627527959506
    assert borrow_info.status == "ACTIVE"


def test_margin_get_interest_history(mock_margin_get_interest_history, margin_service):
    response = margin_service.get_interest_history()
    interest_info = response.result.list[0]
    assert interest_info.loan_id == "1667358632666702944"
    assert interest_info.currency == "BTC"
    assert interest_info.interest == 0
    assert interest_info.time == 1627538759506
    assert interest_info.stake_amount == 50000000
    assert interest_info.interest_rate == Decimal("0.00000334")


def test_margin_get_repay_history(mock_margin_get_repay_history, margin_service):
    response = margin_service.get_repay_history()
    repay_info = response.result.repay_list[0]
    assert repay_info.repay_id == "1667358655209851328"
    assert repay_info.currency == "BTC"
    assert repay_info.repay_amount == 2
    assert repay_info.repay_time == 1627527960178
    assert repay_info.status == "CONFIRMED"
    assert repay_info.outstanding_debt == Decimal("0.00019372")
    assert repay_info.principal_repayment == Decimal("1.99999332")
    assert repay_info.outstanding_principal == Decimal("0.00019372")
    assert repay_info.interest_repayment == Decimal("0.00000668")
    assert repay_info.outstanding_interest == Decimal("0")
    assert repay_info.repay_source == "Normal"


def test_margin_get_liquidation_history(mock_margin_get_liquidation_history, margin_service):
    response = margin_service.get_liquidation_history()
    liquidation_info = response.result.list[0]
    assert liquidation_info.time == 1627554526102
    assert liquidation_info.liquidation_status == "COMPLETED"
    assert liquidation_info.email_status == 1
    assert liquidation_info.margin_level == "NORMAL"
    assert (
        liquidation_info.message
        == "Your Margin Wallet has been liquidated because your Margin Score dropped to or below 1.1."
    )
    assert liquidation_info.message_code == 2


def test_margin_get_liquidation_orders(mock_margin_get_liquidation_orders, margin_service):
    response = margin_service.get_liquidation_orders()
    order_info = response.result.order_list[0]
    assert order_info.status == "FILLED"
    assert order_info.side == "SELL"
    assert order_info.price == Decimal("0.0")
    assert order_info.quantity == Decimal("0.0747")
    assert order_info.order_id == "1668250027295669696"
    assert order_info.client_oid == "LQ: 1627554524101"
    assert order_info.create_time == 1627554525137
    assert order_info.update_time == 1627554525213
    assert order_info.type == "MARKET"
    assert order_info.instrument_name == "ETH_USDT"
    assert order_info.avg_price == Decimal("400.0")
    assert order_info.cumulative_quantity == Decimal("0.0747")
    assert order_info.cumulative_value == Decimal("29.88")
    assert order_info.fee_currency == "USDT"
    assert order_info.exec_inst == ""
    assert order_info.time_in_force == "GOOD_TILL_CANCEL"


def test_create_order(mock_margin_create_order, margin_service):
    response = margin_service.create_order(
        instrument_name="CRO_USDT", price="0.3", quantity="20", side="BUY", type="LIMIT"
    )
    assert response.result.order_id == "1667855088105953856"
    assert response.code == 0


def test_cancel_order(mock_margin_cancel_order, margin_service):
    response = margin_service.cancel_order(instrument_name="CRO_USDT", order_id="1667855088105953856")
    assert response.code == 0


def test_cancel_all_orders(mock_margin_cancel_all_orders, margin_service):
    response = margin_service.cancel_all_orders(instrument_name="BTC")
    assert response.code == 0


def test_get_order_history(mock_margin_get_order_history, margin_service):
    response = margin_service.get_order_history()
    order_info = response.result.order_list[0]
    assert order_info.status == "FILLED"
    assert order_info.side == "BUY"
    assert order_info.price == Decimal("200000.00")
    assert order_info.quantity == Decimal("0.002000")
    assert order_info.order_id == "1664980974402252544"
    assert order_info.client_oid == ""
    assert order_info.create_time == 1627457099768
    assert order_info.update_time == 1627457099831
    assert order_info.type == "LIMIT"
    assert order_info.instrument_name == "BTC_USDT"
    assert order_info.avg_price == Decimal("200000.00000000")
    assert order_info.cumulative_quantity == Decimal("0.002000")
    assert order_info.cumulative_value == Decimal("400.00000000")
    assert order_info.fee_currency == "CRO"
    assert order_info.exec_inst == ""
    assert order_info.time_in_force == "GOOD_TILL_CANCEL"


def test_get_open_orders(mock_margin_get_open_orders, margin_service):
    response = margin_service.get_open_orders()
    order_info = response.result.order_list[0]
    assert order_info.status == "ACTIVE"
    assert order_info.side == "BUY"
    assert order_info.price == Decimal("13.770")
    assert order_info.quantity == Decimal("5.000")
    assert order_info.order_id == "1650488516770762784"
    assert order_info.client_oid == ""
    assert order_info.create_time == 1627025190874
    assert order_info.update_time == 1627025190928
    assert order_info.type == "LIMIT"
    assert order_info.instrument_name == "DOT_USDC"
    assert order_info.avg_price == 0e-8
    assert order_info.cumulative_quantity == Decimal("0.000")
    assert order_info.cumulative_value == 0e-8
    assert order_info.fee_currency == "CRO"
    assert order_info.exec_inst == ""
    assert order_info.time_in_force == "GOOD_TILL_CANCEL"
    assert response.result.count == 2


def test_get_order_detail(mock_margin_get_order_detail, margin_service):
    response = margin_service.get_order_detail(order_id="1664980974402252544")
    trade_info = response.result.trade_list[0]
    assert trade_info.side == "BUY"
    assert trade_info.fee == Decimal("8.00000000")
    assert trade_info.trade_id == "1664980976500418080"
    assert trade_info.instrument_name == "BTC_USDT"
    assert trade_info.create_time == 1627457099831
    assert trade_info.traded_price == Decimal("200000.00")
    assert trade_info.traded_quantity == Decimal("0.002000")
    assert trade_info.fee_currency == "CRO"
    assert trade_info.order_id == "1664980974402252544"
    assert trade_info.client_oid == ""
    assert trade_info.liquidity_indicator == "TAKER"
    order_info = response.result.order_info
    assert order_info.status == "FILLED"
    assert order_info.side == "BUY"
    assert order_info.price == Decimal("200000.00")
    assert order_info.quantity == Decimal("0.002000")
    assert order_info.order_id == "1664980974402252544"
    assert order_info.client_oid == ""
    assert order_info.create_time == 1627457099768
    assert order_info.update_time == 1627457099831
    assert order_info.type == "LIMIT"
    assert order_info.instrument_name == "BTC_USDT"
    assert order_info.avg_price == Decimal("200000.00000000")
    assert order_info.cumulative_quantity == Decimal("0.002000")
    assert order_info.cumulative_value == Decimal("400.00000000")
    assert order_info.fee_currency == "CRO"
    assert order_info.exec_inst == ""
    assert order_info.time_in_force == "GOOD_TILL_CANCEL"


def test_get_trades(mock_margin_get_trades, margin_service):
    response = margin_service.get_trades()
    trade_info = response.result.trade_list[0]
    assert trade_info.side == "BUY"
    assert trade_info.fee == Decimal("0.80000000")
    assert trade_info.trade_id == "1665401749164103488"
    assert trade_info.instrument_name == "BTC_USDT"
    assert trade_info.create_time == 1627469639833
    assert trade_info.traded_price == Decimal("20000.00")
    assert trade_info.traded_quantity == Decimal("0.000200")
    assert trade_info.fee_currency == "CRO"
    assert trade_info.order_id == "1665401746210855264"
    assert trade_info.client_oid == ""
    assert trade_info.liquidity_indicator == "TAKER"


def test_get_margin_trading_user(mock_get_margin_trading_user, margin_service):
    response = margin_service.get_margin_trading_user()
    assert response.code == 0
    assert response.result.margin_leverage == 5


def test_adjust_margin_leverage(mock_adjust_margin_leverage, margin_service):
    response = margin_service.adjust_margin_leverage(3)
    assert response.code == 0
