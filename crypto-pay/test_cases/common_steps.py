import html
import os
import logging
import random
from decimal import Decimal

from pytest import fixture
from pytest_bdd import given, when, parsers, then

from common.utils.on_chain_payment_tools import OnChainTestPaymentTools
from common.utils.tools import Tools

logger = logging.getLogger(__name__)


@fixture(scope="module")
def common_test_data(global_data):
    current_test = os.environ.get("PYTEST_CURRENT_TEST")
    pages = global_data[current_test]["pages"]
    ops_token = os.environ.get("OPS_TOKEN")

    t = {"pages": pages, "ops_token": ops_token}

    yield t


@when(parsers.parse("Navigate to {url}"))
def navigate_to_url(url: str, common_test_data: dict):
    pages = common_test_data["pages"]
    pages.common_page.navigate_to_url(url)
    Tools.sleep(2)


@given(parsers.parse("Navigate to ops {url}"))
@when(parsers.parse("Navigate to ops {url}"))
def navigate_to_ops_url(url: str, common_test_data: dict):
    pages = common_test_data["pages"]
    pages.ops_common_page.navigate_to_ops(url)
    Tools.sleep(2)


@then(parsers.parse("I should see test data bar displayed in {some_page} page"))
def see_test_data_bar(some_page: str, common_test_data: dict):
    pages = common_test_data["pages"]
    pages.common_page.verify_test_data_bar_text()


@then(parsers.parse("I should see test data bar in {some_page} form"))
def see_test_data_bar_form(common_test_data: dict):
    pages = common_test_data["pages"]
    pages.common_page.verify_test_data_bar_form_text()


@when(parsers.parse("Logout at current page"))
def logout_at_current_page(common_test_data: dict):
    pages = common_test_data["pages"]
    pages.common_page.logout_at_current_page()


@when(parsers.parse("Create a new user"))
def create_new_user_for_current(common_test_data: dict):
    pages = common_test_data["pages"]
    ops_token = common_test_data["ops_token"]
    test_data = pages.common_page.test_data

    if "user_name" in test_data.keys():
        test_data["original_user_name"] = test_data["user_name"]
    if "shop_name" in test_data.keys():
        test_data["original_shop_name"] = test_data["shop_name"]
    pages.common_page.create_new_user_by_api(ops_token)


@then(parsers.parse("{action} risk address from ops"))
def add_remove_risk_address_from_ops(action: str, common_test_data: dict):
    pages = common_test_data["pages"]
    apis = pages.common_page.apis
    ops_token = common_test_data["ops_token"]
    test_data = pages.common_page.test_data

    risk_address = test_data["risk_address"]
    if isinstance(risk_address, list):
        for address in risk_address:
            apis.payment_ops.risk_on_chain_address_mag(address, ops_token, action.lower())
    else:
        apis.payment_ops.risk_on_chain_address_mag(risk_address, ops_token, action.lower())


@then(parsers.parse("Cancel payout for wallets"))
def cancel_auto_payout(common_test_data: dict):
    pages = common_test_data["pages"]
    apis = pages.apis
    wallet_address_list = pages.test_data["payout_wallet_address_list"]
    support_token = os.environ.get("SUPPORT_TOKEN")
    wallet_addresses = list()
    for address in wallet_address_list:
        address = ("wallet_addresses[]", address)
        wallet_addresses.append(address)
    apis.payment.cancel_auto_payout(wallet_addresses=wallet_addresses, support_token=support_token)


@then(parsers.parse("Click on the expected transaction and see {explorer} page correct at Ops"))
def click_txn_and_see_explorer_correct(explorer: str, common_test_data: dict):
    pages = common_test_data["pages"]
    test_data = pages.common_page.test_data

    payment_id = test_data["payment_id"]
    pages.ops_common_page.click_inbound_onchain_txn_link(payment_id, explorer)


@then(parsers.parse("My wallet should be received {token} transaction for {txn_type} and amount {amount} {currency}"))
def onchain_wallet_received_correct(token: str, txn_type: str, amount: str, currency: str, common_test_data: dict):
    """
    Amount currency was selected from payment when txn_type is outbound,
    Will update the amount currency conversion when use inbound
    """
    pages = common_test_data["pages"]
    apis = pages.common_page.apis

    ops_token = common_test_data["ops_token"]
    payment_id = pages.common_page.test_data["payment_id"]
    expected_refund_cost = 0

    withdraw_token = pages.common_page.test_data.get("withdraw_token", None)
    pay_core_enable = str(pages.common_page.pay_core_enable()).lower()
    other_chain = False
    if ":other_chain" in txn_type:
        txn_type = txn_type.split(":")[0]
        other_chain = True

    if txn_type == "outbound":
        outbound_details = apis.payment_ops.get_onchain_outbound(
            ops_token, payment_id=payment_id, pay_core_enable=pay_core_enable
        )[0]
        expected_refund_cost = Decimal(
            apis.payment.get_on_chain_refund_network_cost(outbound_details["cryptoCurrency"], withdraw_token)
        )
        crypto_currency = "CRO" if "CRO" in outbound_details["cryptoCurrency"] else outbound_details["cryptoCurrency"]
        txn_id = outbound_details["txnId"]
        txn_id = txn_id.replace("/0", "") if "/0" in txn_id else txn_id
    else:
        inbound = pages.common_page.get_inbound(payment_id=payment_id)
        inbound_details = inbound["data"]["inboundFunds"]["nodes"][0]
        crypto_currency = "CRO" if "CRO" in inbound_details["currency"] else inbound_details["currency"]
        txn_id = pages.common_page.test_data["onchain_inbound_fund_txn_id"]

    if "<" in amount and ">" in amount:
        # Can replace amount from test data e.g rebound_amount or inbound_amount
        expected_amount = Tools.convert_text_from_dict(amount, pages.common_page.test_data)
    else:
        expected_amount = apis.payment.get_converted_amount(currency, crypto_currency, amount)

    # Need to - the network fee when the txn_type is refund
    if expected_refund_cost != 0:
        expected_amount = Decimal(expected_amount) - expected_refund_cost

    if not other_chain:
        new_w3 = pages.common_page.test_data.get("new_w3", False)
        if new_w3 == "true":
            infura_url = pages.common_page.test_data["infura_url"]
            chain_id = pages.common_page.test_data["chain_id"]
            onchain_tools = OnChainTestPaymentTools(infura_url, int(chain_id))
        else:
            onchain_tools = OnChainTestPaymentTools()
    else:
        other_chain_data = pages.common_page.test_data.get("other_chain_data")
        infura_url = other_chain_data["infura_url"]
        chain_id = other_chain_data["chain_id"]
        onchain_tools = OnChainTestPaymentTools(infura_url, int(chain_id))

    Tools.sleep(timeout=60)
    actual_amount = onchain_tools.get_txn_value(txn_id, token)
    base_log = f"【Verify if wallet received {token} amount correct, Actual {actual_amount}, Expected {expected_amount}】"
    if abs(Decimal(actual_amount) - Decimal(expected_amount)) > 1.00:
        logger.error(f"{base_log} - Failed")
        raise Exception(f"{base_log} - Failed")
    else:
        logger.info(f"{base_log} - Passed")


@when(parsers.parse("Trigger current payout to {status}"))
def trigger_payout_status(status: str, common_test_data: dict):
    pages = common_test_data["pages"]
    apis = pages.common_page.apis
    ops_token = common_test_data["ops_token"]

    if "payout_desc" not in pages.common_page.test_data.keys():
        shop_name = pages.common_page.test_data["shop_name"]
        all_payouts = apis.payment_ops.get_payouts(ops_token)
        nodes = all_payouts["data"]["payouts"]["nodes"]
        matched_node = list(filter(lambda node: node["merchantName"] == shop_name, nodes))
        payout_id = matched_node[0]["id"]
    else:
        payout_desc = pages.common_page.test_data["payout_desc"]
        pay_core_enable = str(pages.common_page.pay_core_enable()).lower()
        payout_id, current_status = apis.payment_ops.get_payout_id_by_desc(
            desc=payout_desc, ops_token=ops_token, pay_core_enable=pay_core_enable
        )

    apis.payment_ops.update_payout_status_by_id(status=status, payout_id=payout_id, ops_token=ops_token)
    payout_id, current_status = apis.payment_ops.get_payout_by_id(
        payout_id=payout_id,
        ops_token=ops_token,
    )
    pages.common_page.test_data["payout_id"] = payout_id

    base_log = (
        f"【Verify payout status is updated after trigger the update payout status api】: "
        f"Actual {current_status}, Expected {status}"
    )
    if current_status != status:
        logger.error(f"{base_log} - Failed")
        raise AssertionError(f"{base_log} - Failed")
    else:
        logger.info(f"{base_log} - Passed")

    pages.common_page.navigate_to_url("<global_host>/balance/payout_history")


@when(parsers.parse("Trigger the expected payout to {status}"))
def trigger_payout_status(status: str, common_test_data: dict):
    pages = common_test_data["pages"]
    apis = pages.common_page.apis
    ops_token = common_test_data["ops_token"]

    payout_id = pages.common_page.test_data["payout_id"]
    payout_id, current_status = apis.payment_ops.get_payout_by_id(
        payout_id=payout_id,
        ops_token=ops_token,
    )
    apis.payment_ops.update_payout_status_by_id(status=status, payout_id=payout_id, ops_token=ops_token)
    payout_id, current_status = apis.payment_ops.get_payout_by_id(
        payout_id=payout_id,
        ops_token=ops_token,
    )
    base_log = (
        f"【Verify payout status is updated after trigger the update payout status api】: "
        f"Actual {current_status}, Expected {status}"
    )
    if current_status != status:
        logger.error(f"{base_log} - Failed")
        raise AssertionError(f"{base_log} - Failed")
    else:
        logger.info(f"{base_log} - Passed")

    pages.common_page.navigate_to_url("<global_host>/balance/payout_history")


@when(parsers.parse("Clear the {key_name} key from test data"))
def clear_key_from_test_data(key_name: str, common_test_data: dict):
    pages = common_test_data["pages"]
    test_data = pages.common_page.test_data

    if key_name in test_data.keys():
        temp_test_data = test_data
        del temp_test_data[key_name]
        pages.common_page.test_data = temp_test_data
        logger.info(f"【{key_name} was removed from test data】")
    else:
        logger.warning(f"【{key_name} doesn't exist in test data】")


@then(parsers.parse("I should see payment {column_text} is {expected_value} in ops outbound page"))
def verify_payment_in_ops_outbound(column_text: str, expected_value: str, common_test_data: dict):
    pages = common_test_data["pages"]
    test_data = pages.common_page.test_data

    pages.ops_common_page.navigate_to_ops("<global_ops_host>/onchain_outbound")
    payment_id = test_data["payment_id"]
    pages.common_page.search_item_by(payment_id)
    index_map = {"amount": 4, "request_amount": 5, "currency": 7, "status": 9, "reason": 10}

    expected_value = Tools.convert_text_from_dict(expected_value, test_data)
    test_data["outbound_column_index"] = index_map[column_text]
    first_expected_outbound_text = pages.ops_common_page.get_element("first_expected_outbound_text").text
    base_log = (
        f"Verify {column_text} in ops outbound page if correct, Actual is {first_expected_outbound_text}, "
        f"Expected is {expected_value}"
    )

    if first_expected_outbound_text != expected_value:
        raise AssertionError(f"{base_log} - Failed")
    else:
        logger.info(f"{base_log} - Passed")


@when(parsers.parse("I go to ops outbound page and {mark_as_option} the rebound via {type_value}"))
def modify_payments_status_in_ops_outbound(mark_as_option: str, type_value: str, common_test_data: dict):
    pages = common_test_data["pages"]
    test_data = pages.common_page.test_data
    payment_id = Tools.convert_text_from_dict(type_value, test_data)

    ops_url = Tools.convert_text_from_dict("<global_ops_host>", test_data)
    pages.common_page.driver.execute_script("window.open('%s');" % ops_url)
    pages.common_page.switch_to_windows("next")
    pages.ops_common_page.navigate_to_ops("<global_ops_host>/onchain_outbound")

    pages.common_page.search_item_by(payment_id)
    if mark_as_option == "reject":
        pages.ops_common_page.get_element("mark_as_reject_btn").click()
    else:
        pages.ops_common_page.get_element("mark_as_approve_btn").click()
    pages.common_page.switch_to_windows("default")
    actual_reject = pages.checkout_page.get_element("refound_reject").wait_el(action="wait_interval", timeout=10)
    pages.checkout_page.assert_text("equals", actual_reject, "Refund Rejected")


@then(parsers.parse("I go to ops refund page and verify amount {amount} if correct"))
def go_ops_refund_verify_amount(amount: str, common_test_data: dict):
    pages = common_test_data["pages"]
    test_data = pages.common_page.test_data
    payment_id = test_data["payment_id"]
    amount = Tools.convert_text_from_dict(amount, test_data)

    pages.ops_common_page.navigate_to_ops("<global_ops_host>/refunds")
    pages.ops_common_page.search_and_verify_text_by_td_index(value=payment_id, index=9, expected_text=amount)


@when(parsers.parse("Set random group test data"))
def set_random_group_test_data(common_test_data: dict):
    pages = common_test_data["pages"]
    test_data = pages.common_page.test_data
    random_group: list = test_data.get("random_group")
    group: dict = random.choice(random_group)

    for key, value in group.items():
        test_data[key] = value


@when(parsers.parse("Set runtime key {key_name} and value {value_name}"))
def set_runtime_key_value(key_name: str, value_name: str, common_test_data: dict):
    pages = common_test_data["pages"]

    test_data = pages.common_page.test_data
    test_data[key_name] = value_name


@then(parsers.parse("Verify {verify_type} {message_type} slack channel message"))
def verify_slack_channel_message(common_test_data: dict, verify_type: str, message_type: str):
    pages = common_test_data["pages"]
    apis = pages.apis
    slack_bot_token = os.environ["SLACK_BOT_TOKEN"]
    if message_type == "new_partner":
        channel_id = os.environ["SLACK_NEW_PARTNER_CHANNEL_ID"]
    else:
        raise NotImplementedError("Please specific your slack channel id")
    shop_name = pages.test_data["shop_name"]
    slack_message = apis.subscriptions.get_slack_message(slack_bot_token=slack_bot_token, channel_id=channel_id)
    if verify_type == "see":
        filtered_conversation_history = list(filter(lambda x: shop_name in x["text"], slack_message))
        history_text = filtered_conversation_history[0]["text"]
        slack_message = html.unescape(history_text).replace("*", "")
    else:
        history_text = slack_message[0]["text"]
        slack_message = html.unescape(history_text).replace("*", "")
    pages.common_page.verify_slack_channel_message(verify_type, message_type, slack_message)


@then(parsers.parse("Save reward level correct on off-chain payment"))
def verify_reward_level_correct(login_test_data: dict, common_test_data: dict):
    pages = login_test_data["pages"]
    rate = pages.common_page.get_pay_reward_rate()

    pages.common_page.test_data["reward_rate"] = rate


@then(parsers.parse("I {receive_type} received {email_type} email from gmail"))
def verify_received_gmail_email(common_test_data: dict, receive_type: str, email_type: str):
    pages = common_test_data["pages"]
    if email_type == "payout_approved":
        to_addr = pages.test_data["user_name"]
        subject = "[Crypto.com Pay] Payout Setting approved"
    elif email_type == "payout_rejected":
        to_addr = pages.test_data["user_name"]
        subject = "[Crypto.com Pay] Payout Setting rejected"
    elif email_type == "crypto_purchase_otp":
        to_addr = pages.test_data["email_address"]
        subject = "Your Email Verification Code"
    else:
        to_addr = pages.test_data["email_address"]
        subject = ""

    if "not" in receive_type:
        receive_type = "failed"
    else:
        receive_type = "success"
    pages.common_page.verify_email_receive(receive_type, subject, email=to_addr)


@then(parsers.parse("Verify {email_type} email details from gmail"))
def verify_email_details(common_test_data: dict, email_type: str):
    pages = common_test_data["pages"]
    if email_type == "payout_approved":
        to_addr = pages.test_data["user_name"]
        subject = "[Crypto.com Pay] Payout Setting approved"
    elif email_type == "payout_rejected":
        to_addr = pages.test_data["user_name"]
        subject = "[Crypto.com Pay] Payout Setting rejected"
    else:
        to_addr = pages.test_data["email_address"]
        subject = ""
    pages.common_page.verify_received_email(email_type, email_address=to_addr, subject=subject)
