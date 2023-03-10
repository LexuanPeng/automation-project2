import os
import logging
from datetime import datetime, date
from decimal import Decimal
import json

from common.utils.gmail_helper import GmailHelper
from common.utils.on_chain_payment_tools import OnChainTestPaymentTools
from cdc.qa.integrations.otp import get_totp
from common.utils.main_app_tools import MainAppTools
from common.utils.tools import Tools
from pages.base_page import BasePage
from dateutil import parser

logger = logging.getLogger(__name__)


class CommonPage(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_name = "common"

    def navigate_to_url(self, url: str):
        url = Tools.convert_text_from_dict(url, self.test_data)
        self.driver.get(url)
        Tools.sleep(1)

    def select_shop_by_name(self, shop_name: str):
        # Select shop at side bar
        Tools.sleep(1)
        if shop_name == "Crypto.com Shop":
            # Since this shop have lot of data need to load
            Tools.sleep(8)

        self.get_element("user_link").wait_el(timeout=2).actions_by_el("hover")

        self.test_data["shop_name"] = shop_name
        user_item = self.get_element("user_item").wait_el(timeout=2)
        user_item.actions_by_el("hover_click")

        Tools.sleep(3)
        self.test_data["menu_text"] = "profile"
        self.get_element("side_menu_item").wait_el(timeout=1).actions_by_el("hover")
        self.assert_text("contains", self.get_element("user_link").wait_el(timeout=2), shop_name)

    def logout_at_current_page(self):
        self.get_element("user_link").wait_el(timeout=2).actions_by_el("hover")

        login_field = self.get_element("login_field", "login")
        check_login_field = self.check_el_execute(login_field)
        if not check_login_field:
            self.get_element("logout_link").wait_el(timeout=2).actions_by_el("hover_click")

        self.assert_object("see", login_field.wait_el(timeout=5))

    def go_page_and_click_tab(self, side_item_text: str, main_title: str, tab_name: str):
        # Go some pages like Balances, Settings and click the tab to go sub pages
        self.click_tab(side_item_text)

        self.test_data["main_title"] = main_title
        main_title = self.get_element("main_title").wait_el(timeout=2)
        self.assert_object("see", main_title)

        self.test_data["tab_name"] = tab_name
        self.get_element("sub_header_tab").wait_el(timeout=2).click()
        Tools.sleep(3)

    def click_tab(self, side_item_text):
        self.test_data["menu_text"] = side_item_text
        self.get_element("side_menu_item").wait_el(timeout=1).click()

    def input_password(self):
        # Input the password while pop up the password form, This will add 2fa to header
        self.get_element("input_password_layout").wait(timeout=4)
        self.get_element("password_field").input(self.test_data["password"])
        self.get_element("password_confirm_btn").click()
        Tools.sleep(3)

    def input_password_with_2fa(self, seed: str):
        self.get_element("input_password_layout").wait(timeout=2)
        self.get_element("password_field").input(value=self.test_data["password"], clear=True)
        code: str = get_totp(seed)
        self.get_element("code2fa_field").input(value=code, clear=True)
        self.get_element("password_confirm_btn").click()

        # Loop to input the verification code
        error_2fa = self.get_element("error_2fa")
        check_error_2fa = self.check_el_execute(error_2fa, True)
        while check_error_2fa:
            Tools.sleep(3)
            code: str = get_totp(seed)
            self.get_element("code2fa_field").input(value=code, clear=True)
            self.get_element("password_confirm_btn").click()
            Tools.sleep(1)
            check_error_2fa = self.check_el_execute(error_2fa, True)
        Tools.sleep(1)

    def input_incorrect_password_and_2fa(self):
        self.get_element("input_password_layout").wait(timeout=2)
        self.get_element("password_field").input(value="123456", clear=True)
        self.get_element("code2fa_field").input(value="123456", clear=True)
        self.get_element("password_confirm_btn").click()

        error_2fa = self.get_element("error_2fa")
        self.assert_object("see", error_2fa)

    def click_filter_btn(self):
        # Click on the filter button at the sub pages
        self.get_element("filter_btn").click()
        self.assert_object("see", self.get_element("filter_clear_btn"))
        self.assert_object("see", self.get_element("filter_apply_btn"))

    def select_multiple_filter_conditions(self):
        """
        Select filters to check the data in sub page, must create multiple_filter_conditions in test data
        e.g:
        multiple_filter_conditions:
            Amount:
              type: selection
              option: is equal to
              field1: "30"
            Status:
              type: selection
              option: Not Refunded
            Date:
              type: date              # Will select the start date before current year
            Payment Method:
              type: selection
              option: Checkout
            (some condition has two fields):
                type: range
                field1: "2222"
                field2: "3333"
        """
        if "multiple_filter_conditions" not in self.test_data.keys():
            raise ValueError("【multiple_filter_conditions details needed in test data】")

        conditions: dict = self.test_data["multiple_filter_conditions"]

        for name, condition in conditions.items():
            self.test_data["item_text"] = name
            self.get_element("filter_item_box").wait_el(timeout=1).click()

            actions = condition.keys()
            action_type = condition["type"]
            if action_type == "selection":
                self.test_data["option_text"] = condition["option"]
                self.get_element("filter_item_selection").click()
                self.get_element("filter_item_option").wait_el(timeout=1).click()
                if "field1" in actions:
                    field1 = condition["field1"]
                    self.get_element("filter_item_input_field1").actions_by_el("double_click")
                    self.get_element("filter_item_input_field1").input_key("back_space")
                    self.get_element("filter_item_input_field1").input(value=field1, clear=True)
                if "field2" in actions:
                    field2 = condition["field2"]
                    self.get_element("filter_item_input_field2").actions_by_el("double_click")
                    self.get_element("filter_item_input_field2").input_key("back_space")
                    self.get_element("filter_item_input_field2").input(value=field2, clear=True)
            elif action_type == "range":
                field1 = condition["field1"]
                field2 = condition["field2"]
                self.get_element("filter_item_input_field1").input(field1)
                self.get_element("filter_item_input_field1").actions_by_el("double_click")
                self.get_element("filter_item_input_field1").input_key("back_space")

                self.get_element("filter_item_input_field2").actions_by_el("double_click")
                self.get_element("filter_item_input_field2").input_key("back_space")
                self.get_element("filter_item_input_field2").input(field2)
            elif action_type == "date":
                self.get_element("filter_date_input_filed1").click()
                Tools.sleep(1)
                # To make sure we have data from the range
                while True:
                    current_left_year = self.get_element("calendar_left_year").text
                    if current_left_year != str(date.today().year - 1):
                        self.get_element("calendar_pre_month_btn").wait_el(timeout=1).click()
                    else:
                        day = self.get_element("calendar_pre_left_first").text
                        month = self.get_element("calendar_left_month").text
                        self.test_data["expected_date"] = f"{month} {day} {current_left_year}"
                        self.get_element("calendar_pre_left_first").click()
                        break
                Tools.sleep(1)

                while True:
                    calendar_right_year = self.get_element("calendar_right_year").text
                    calendar_right_month = self.get_element("calendar_right_month").text
                    today = date.today()
                    if calendar_right_year != str(today.year) or calendar_right_month != today.strftime("%b"):
                        self.get_element("calendar_next_month_btn").wait_el(timeout=1).click()
                    else:
                        self.get_element("calendar_future_right_first").click()
                        break
            else:
                raise ValueError(f"【Current action type was not supported】: {action_type}")

        self.get_element("filter_apply_btn").wait_el(timeout=2).click()
        Tools.sleep(1)

    def verify_alert_error_not_exist(self):
        self.assert_object("notsee", self.get_element("error_alert_msg"))

    def switch_test_data_tab(self, status: str = "on"):
        if status == "on":
            off_tab = self.get_element("switch_test_data_tab")
            check_execute = self.check_el_execute(off_tab, True)

            if check_execute:
                self.get_element("switch_test_data_tab").click()
        else:
            on_tab = self.get_element("switch_test_data_tab_off")
            check_execute = self.check_el_execute(on_tab, True)

            if check_execute:
                self.get_element("switch_test_data_tab_off").click()

    def verify_test_data_bar_text(self):
        test_data_bar = self.get_element("test_data_bar")
        self.assert_text("equals", test_data_bar, "Test Data")

    def verify_test_data_bar_form_text(self):
        Tools.sleep(1)
        test_data_bar_form = self.get_element("test_data_bar_form").wait(timeout=3)
        self.assert_text("equals", test_data_bar_form, "Test Data")

    def search_item_by(self, input_value: str):
        """
        Search item in page with search field
        @param input_value: input value
        """
        # Only check if pay core enable filter in below list:
        # check_url_list = ["onchain_inbound", "refunds", "onchain_outbound", "payments"]
        check_url_list = ["payouts"]
        current_url = self.driver.current_url
        go_to_check = False
        for url in check_url_list:
            r = f".+ops.+({url})"
            is_matched = Tools.match_text_by_re(r, current_url, "search")
            if is_matched is not None:
                go_to_check = True
                break
        if go_to_check and self.pay_core_enable() is False:
            # multiple_filter_conditions = {"BE System": {"type": "selection", "option": "Pay Server"}}
            # self.test_data["multiple_filter_conditions"] = multiple_filter_conditions
            # self.click_filter_btn()
            # self.select_multiple_filter_conditions()
            self.click_filter_btn()
            self.test_data["item_text"] = "BE System"
            self.test_data["option_text"] = "Pay Server"
            self.get_element("filter_item_selection").click()
            self.get_element("filter_item_option").wait_el(timeout=1).click()
            self.get_element("filter_apply_btn").wait_el(timeout=2).click()
            Tools.sleep(1)

        self.get_element("filter_input").wait_el(timeout=1).input(
            value=input_value, enter=True, clear=True, clear_count=3
        )
        first_row = self.get_element("first_row")
        self.assert_object("see", first_row)
        Tools.sleep(2)

    def click_1st_item_of_table(self):
        """Click the 1st item on the table"""
        first_row = self.get_element("first_row").wait_el(timeout=2)
        first_row.click()
        Tools.sleep(1)

    def verify_transaction_record_exist_in_main_app(self, token: str, user_id: str, txn_type: str):
        base_log = f"【Verify user_id {user_id} transaction record exist in Main App】: {txn_type}"
        txn_records: list = MainAppTools.get_transaction_record(token=token)
        filter_result = list(filter(lambda x: x["user_uuid"] == user_id, txn_records))

        if len(filter_result) == 0:
            logger.error(f"{base_log} - Not Exist - {txn_records}")
            raise AssertionError(f"{base_log} - Not Exist - {txn_records}")
        else:
            logger.info(f"{base_log} - Exist")
            if txn_type == "refund" or txn_type == "rebound":
                filter_txn_type_result = list(
                    filter(
                        lambda x: x["nature"] == "income"
                        and txn_type in x["kind"]
                        and f"Refund from {self.test_data['shop_name']}" in x["description"],
                        filter_result,
                    )
                )
            else:
                filter_txn_type_result = list(
                    filter(
                        lambda x: x["nature"] == "payment"
                        and txn_type in x["kind"]
                        and self.test_data["shop_name"] in x["description"],
                        filter_result,
                    )
                )

        base_log = f"【Verify user_id {user_id} transaction record contains {txn_type}】"
        if len(filter_txn_type_result) == 0:
            logger.error(f"{base_log} - Failed - {filter_result}")
            raise AssertionError(f"{base_log} - Failed - {filter_result}")
        else:
            logger.info(f"{base_log} - Passed")

        return filter_txn_type_result[0]

    def verify_transaction_record_amount(
        self,
        token: str,
        from_currency: str,
        amount: str,
        txn_record: dict,
        txn_type: str,
    ):
        """Verify transaction record amount in main app"""
        base_log = f"【Verify transaction record amount from {from_currency} in main app】:"
        actual_amount = Decimal(txn_record["amount"]["amount"])
        if txn_type == "refund":
            pay_merchant_refund_currency = MainAppTools.get_user_config(token)["user_config"][
                "pay_merchant_refund_currency"
            ]
            live_rates = MainAppTools.get_live_rates(token, from_currency, pay_merchant_refund_currency)
            lot_size = live_rates["lot_size"]
            rate = Decimal(live_rates["rates"][0]["tiers"][0]["rate"])
            amount = (Decimal(amount) * rate).quantize(Decimal(lot_size))
        else:
            # TODO Verify payment amount
            pass
        if abs(Decimal(amount) - actual_amount) > 0.5:
            logger.error(f"{base_log} - Failed, Actual {actual_amount}, Expected {amount}, {txn_record}")
            raise AssertionError(f"{base_log} - Failed, Actual {actual_amount}, Expected {amount}, {txn_record}")
        else:
            logger.info(f"{base_log} - Passed, Actual {actual_amount}, Expected {amount}")

    def create_new_user_by_api(
        self,
        ops_token: str = None,
        user_name: str = None,
        password: str = None,
        external_info: dict = None,
        create_team: bool = True,
        business_role: str = "merchant",
    ):
        support_token = os.environ.get("SUPPORT_TOKEN")
        fm = datetime.now().strftime("%Y%m%d%H%M%S%f")
        if user_name is None:
            user_name = f"auto{fm}@email.com"
        if password is None:
            password = "Tester@#$1"

        account_info = {
            "email": user_name,
            "password": password,
            "first_name": f"firstName{fm}",
            "last_name": f"lastName{fm}",
            "business_role": business_role,
        }

        if create_team:
            # External info only for creating team
            if external_info is not None:
                account_info.update(external_info)

            d = self.apis.payment.create_registration_and_team(account_info, support_token)
            team_details = d["team_details"]
            team_id = team_details["id"]
            shop_name = team_details["name"]
            account_id = team_details["liveAccount"]["id"]
            self.test_data["user_id"] = d["data"]["createRegistration"]["user_id"]

            self.apis.payment_ops.ops_update_team(team_id=team_id, token=ops_token)
            self.test_data["shop_name"] = shop_name
            self.test_data["account_id"] = account_id
            self.test_data["team_id"] = team_id

            pk_key, sk_key, token, two_fa_token = self.apis.payment.get_pk_key(user_name, password, account_id)
            self.test_data["pk_key"] = pk_key
            self.test_data["secret_key"] = sk_key
            self.test_data["token"] = token
            self.test_data["two_fa_token"] = two_fa_token
        else:
            self.apis.payment.create_registration(account_info, support_token)

        self.test_data["user_name"] = user_name
        self.test_data["password"] = password
        logger.debug(f"【Current new user: 】: user_name: {user_name}")

    def create_team_in_page(self, team_info: dict):
        user_link = self.get_element("user_link")
        if self.check_el_execute(user_link, True):
            user_link.actions_by_el("hover")
            self.get_element("new_account_link").wait_el(timeout=2).actions_by_el("hover_click")
            self.get_element("create_business_field").wait_el(timeout=1).actions_by_el("hover")

        shop_name = team_info.get("shop_name", "auto_" + datetime.now().strftime("%Y%m%d%H%M%S%f"))
        website = team_info.get("website", "www.automation.com")
        preferred_currency = team_info.get("preferred_currency", "USD")
        business_category = team_info.get("business_category", "Corporation/Company (LLC/LTD/Etc.)")
        # business_role = team_info.get("business_role", "Merchant")
        business_role = team_info.get("business_role", "merchant")
        daily_volume = team_info.get("daily_volume", "> USD 1,000,000")
        # daily_customer = team_info.get("daily_customer", "< 10")
        # monthly_payout = team_info.get("monthly_payout", "< 2")

        self.get_element("create_business_field").wait_el(timeout=1).input(value=shop_name)
        self.get_element("create_business_website_field").input(value=website)

        self.get_element("default_balances_currency_selection").click()
        self.test_data["option_text"] = preferred_currency
        self.get_element("filter_item_option").wait_el(timeout=2).click()

        self.test_data["option_text"] = business_role
        self.get_element("business_role_option").click()

        self.get_element("type_business_selection").click()
        self.test_data["option_text"] = business_category
        self.get_element("filter_item_option").click()

        self.get_element("daily_volume_selection").click()
        self.test_data["option_text"] = daily_volume
        self.get_element("filter_item_option").wait_el(timeout=1).click()

        # self.get_element("daily_customer_selection").click()
        # self.test_data["option_text"] = daily_customer
        # self.get_element("filter_item_option").wait_el(timeout=1).click()
        #
        # self.get_element("monthly_payout_selection").click()
        # self.test_data["option_text"] = monthly_payout
        # self.get_element("filter_item_option").wait_el(timeout=1).click()

        self.get_element("create_business_btn").click()
        self.test_data["shop_name"] = shop_name
        Tools.sleep(10, sleep_type="timeout")

        verify_after_create_team = self.test_data.get("verify_after_create_team", False)
        if verify_after_create_team:
            self.get_element("go_to_verify").wait_el(timeout=1).click()
            # self.get_element("tell_me_about_you").wait_el(timeout=1).click()
            # self.get_element("tell_us_about_your_business").click()
            info = "Shop" if business_role == "merchant" else "Business"
            self.test_data["title"] = "Profile"
            self.get_element("h3_title").wait_el(timeout=1)
            self.test_data["title"] = f"{info} information"
            self.get_element("h3_title").wait_el(timeout=1)
            self.test_data["title"] = "Business Details"
            self.get_element("h3_title").wait_el(timeout=1)
            self.test_data["title"] = "Business Representative"
            self.get_element("h3_title").wait_el(timeout=1)
            self.test_data["title"] = "Documents Uploads"
            self.get_element("h3_title").wait_el(timeout=1)
            self.test_data["title"] = "Summary"
            self.get_element("h3_title").wait_el(timeout=1)

            self.test_data["title"] = f"Go to {info} Information"
            self.get_element("go_to_verify").wait_el(timeout=1).click()
            self.test_data["title"] = "Company Brand Name"
            brand_name = (
                self.get_element("create_business_input_field", "settings").wait_el(timeout=1).get_attribute("value")
            )
            assert brand_name == shop_name, f"【Verify bran name {brand_name} == {shop_name}】"
            self.test_data["title"] = f"{info} Website"
            business_website = self.get_element("create_business_input_field", "settings").get_attribute("value")
            assert website == business_website, f"【Verify website name {website} == {business_website}】"
            self.test_data["title"] = daily_volume
            daily_volume = self.get_element("business_role_text")
            self.assert_object("see", daily_volume)
            # self.test_data["title"] = daily_customer
            daily_customer = self.get_element("business_role_text")
            self.assert_object("see", daily_customer)
            # self.test_data["title"] = monthly_payout
            monthly_payout = self.get_element("business_role_text")
            self.assert_object("see", monthly_payout)
            self.get_element("business_details_link", "settings").click()
            info = "Merchant" if business_role == "merchant" else "Channel Partner"
            self.test_data["title"] = info
            role = self.get_element("business_role_text").wait_el(timeout=1).text
            assert role == info, f"【Verify business role {role} == {info}】"
            self.test_data["title"] = business_category
            category = self.get_element("business_role_text").text
            assert category == business_category, f"【Verify business category {category} == {category}】"

            if daily_volume == "> 100000 USD":
                self.get_element("document_link", "settings").click()
                self.test_data["title"] = "Business Registration or Equivalent"
                business_registration_or_equivalent = self.get_element("document_type", "settings")
                self.assert_object("see", business_registration_or_equivalent)
                self.test_data["title"] = "Company’s Proof of Address"
                company_proof_of_address = self.get_element("document_type", "settings")
                self.assert_object("see", company_proof_of_address)
                self.test_data["title"] = "Shareholder Registers"
                shareholder = self.get_element("document_type", "settings")
                self.assert_object("see", shareholder)
                if business_role == "merchant":
                    self.test_data["title"] = "Memorandum or Articles of Association"
                    memorandum = self.get_element("document_type", "settings")
                    self.assert_object("see", memorandum)
                    self.test_data["title"] = "Declaration of Source of Funds"
                    declaration = self.get_element("document_type", "settings")
                    self.assert_object("see", declaration)
                    self.test_data["title"] = "Company’s Bank Statement"
                    bank_statement = self.get_element("document_type", "settings")
                    self.assert_object("see", bank_statement)
                else:
                    self.test_data["title"] = "Company's Ownership Structure Chart"
                    ownership = self.get_element("document_type", "settings")
                    self.assert_object("see", ownership)
                    self.test_data["title"] = "AML Policy"
                    aml = self.get_element("document_type", "settings")
                    self.assert_object("see", aml)
                    self.test_data["title"] = "Financial License"
                    financial = self.get_element("document_type", "settings")
                    self.assert_object("see", financial)
                    self.test_data["title"] = "Onboarding procedure for sub-merchants"
                    onboarding = self.get_element("document_type", "settings")
                    self.assert_object("see", onboarding)

            self.get_element("back_btn").click()

    def input_sign_up_fields(self, user_name: str = None, password: str = None, mode: str = "default"):
        self.get_element("geetest_btn", "login").wait(timeout=3).click()
        self.get_element("aggree_pl_checkbox", "login").click()

        fm = datetime.now().strftime("%Y%m%d%H%M%S%f")
        first_name = f"firstName{fm}"
        last_name = f"lastName{fm}"
        self.get_element("first_name_field", "login").input(value=first_name)
        self.get_element("last_name_field", "login").input(value=last_name)
        login_field = self.get_element("login_field", "login")

        if mode == "default":
            if login_field.text == "":
                new_user_email = f"auto{fm}@email.com"
                login_field.input(value=new_user_email)
                self.test_data["user_name"] = new_user_email
            else:
                self.test_data["user_name"] = login_field.text
            password = "Tester@#$1"
        elif mode == "invite":
            # Don't need input user name when sign up by a invite link
            user_name = login_field.text
            alert_message = self.get_element("alert_message").wait_el(timeout=2)
            self.assert_text("contains", alert_message, "You are invited to join ")
            self.assert_text("contains", alert_message, self.test_data["original_shop_name"])
            self.test_data["user_name"] = user_name
        else:
            login_field.input(value=user_name)
            self.test_data["user_name"] = user_name

        self.get_element("password_field", "login").input(value=password)
        # self.get_element("confirm_password_field").input(value=password)
        self.test_data["password"] = password
        Tools.sleep(3)
        self.get_element("sign_up_btn", "login").click()
        Tools.sleep(3)

    def sign_up_for_every_redirect(self, action: str = "valid", activate: str = "activate"):
        self.input_sign_up_fields(mode="default")
        support_token = os.environ["SUPPORT_TOKEN"]
        signup_intent_token, user_id = self.apis.payment.get_signup_intent_token(
            self.test_data["user_name"], support_token
        )
        # To verify when inputting a invalid activate url and return
        if action == "invalid":
            url = Tools.convert_text_from_dict("<global_host>", self.test_data)
            url = f"{url}/user/sign_up/activate?signupIntentToken=abcdefg&userId={user_id}"
            self.driver.get(url)
            Tools.sleep(2)
            error_alert = self.get_element("error_alert_msg")
            self.assert_text("contains", error_alert, "Activation link is invalid or expired, please sign up again")
            return
        if activate == "activate":
            self.apis.payment.activate_registration(signup_intent_token, user_id)
            logger.info(f"【Sign up for new user】{self.test_data['user_name']}")

        self.get_element("back_to_signin_link", "login").click()

    def verify_we_are_at_correct_explorer(self, explorer: str):
        base_log = (
            f"【Verify if we are in the correct explorer " f"{explorer} page after click inbound onchain txn link】: "
        )
        verify_status = False
        if explorer == "goerli.etherscan":
            if "goerli.etherscan" in self.driver.current_url:
                verify_status = True
        elif explorer == "cronos.org":
            if "cronos.org" in self.driver.current_url:
                verify_status = True
        else:
            raise ValueError(f"{base_log}: Unsupported explorer!")
        base_log = f"{base_log} - {self.driver.current_url}"
        if verify_status:
            logger.info(f"{base_log} - Passed")
        else:
            logger.error(f"{base_log} - Failed")
            raise Exception(f"{base_log} - Failed")

    def get_dropdown_value(self, loop_time: int = 100):
        currency_list = []
        for i in range(loop_time):
            current_selection = self.get_element("active_currency_selection", "invoices").get_attribute("title")
            if current_selection not in currency_list:
                currency_list.append(current_selection)
                self.actions(action_type="key_down")
            else:
                break
        return currency_list

    def select_condition_and_search(self, input_value: str = None, multiple_condition: dict = None):
        self.click_filter_btn()

        if multiple_condition is not None:
            self.test_data["multiple_filter_conditions"] = multiple_condition
        self.select_multiple_filter_conditions()

        if input_value is not None:
            self.search_item_by(input_value=input_value)

    def go_to_refund_url(self, refund_type: str = "refund"):
        payment_id = self.test_data.get("payment_id")
        support_token = os.environ["SUPPORT_TOKEN"]
        Tools.sleep(3)

        if refund_type == "rebound":
            inbound = self.get_inbound(payment_id=payment_id)
            nodes = inbound["data"]["inboundFunds"]["nodes"]
            nodes = list(filter(lambda x: x["status"] != "captured", nodes))
            r_d = nodes[0]["id"]
        else:
            refund_data = self.get_inbound(payment_id=payment_id, type_ops="refund")["data"]
            r_d = refund_data["refunds"]["nodes"][0]["id"]

        refund_url = self.apis.payment.get_on_chain_refund_prepare_url(
            r_d=r_d, token=support_token, refund_type=refund_type
        )
        se_token = Tools.match_text_by_re(r"token=(.*)", refund_url, "search", True)
        self.test_data["withdraw_token"] = se_token
        self.test_data["outbound_token"] = se_token
        self.driver.get(url=refund_url)
        return refund_url

    def onchain_pay(self, pay_amount: str = None, to_address: str = None, none_token: bool = False):
        pay_amount = pay_amount if pay_amount is not None else self.test_data.get("to_pay_amount")
        to_address = to_address if to_address is not None else self.test_data.get("to_address")
        from_address = self.test_data["from_address"]
        from_contract_address = None if none_token is True else self.test_data.get("from_contract_address")
        from_address_pk_key = self.test_data["from_address_pk_key"]
        new_w3 = self.test_data.get("new_w3", "false")
        # Change the chain like CRONOS or ERC20
        if new_w3 == "true":
            infura_url = self.test_data["infura_url"]
            chain_id = self.test_data["chain_id"]
            on_chain_test_payment_tools = OnChainTestPaymentTools(infura_url, int(chain_id))
        else:
            on_chain_test_payment_tools = OnChainTestPaymentTools()
        # Send txn by eth or token
        if from_contract_address is not None:
            onchain_inbound_fund_txn_id = on_chain_test_payment_tools.on_chain_test_pay(
                from_address, from_contract_address, from_address_pk_key, to_address, pay_amount, None
            )
        else:
            onchain_inbound_fund_txn_id = on_chain_test_payment_tools.on_chain_test_pay_by_eth(
                from_address, to_address, from_address_pk_key, pay_amount
            )
        self.test_data["onchain_inbound_fund_txn_id"] = onchain_inbound_fund_txn_id
        self.test_data["payment_amount"] = pay_amount
        return onchain_inbound_fund_txn_id

    def verify_decimal_by_currency(self, currency_type: str, currency_amount: str):
        currency_type = self.apis.payment.get_dollar_currency_type(currency_type)  # from $ to USD
        decimal_n = self.apis.payment.get_currency_unit(currency_type)
        if currency_type not in ["EUR", "AUD", "USD", "GBP", "CNY", "CAD"]:
            if "." in currency_amount:
                currency_amount_decimal = currency_amount.split(".")[1]
                if len(currency_amount_decimal) <= decimal_n and currency_amount_decimal[-1] != "0":
                    logger.info(f"verified currency {currency_type} successful")
                else:
                    log = f"Currency {currency_type} verified failed!!!Actual failed value is {currency_amount}"
                    logger.error(log)
                    raise ValueError(log)
        else:
            if "." in currency_amount:
                currency_amount_decimal = currency_amount.split(".")[1]
                if len(currency_amount_decimal) == decimal_n:
                    logger.info(f"verified currency {currency_type} successful")
                else:
                    log = f"Currency {currency_type} verified failed!!!Actual failed value is {currency_amount}"
                    logger.error(log)
                    raise ValueError(log)
            else:
                log = f"Currency {currency_type} verified failed!!!Actual failed value is {currency_amount}"
                logger.error(log)
                raise ValueError(log)

    def get_all_react_option_list(self, drop_down_element: object) -> list:
        all_dropdown_options = []
        while True:
            aria_activedescendant_id = drop_down_element.get_attribute("aria-activedescendant")
            self.test_data["list_id"] = aria_activedescendant_id
            option = self.get_element("drop_down_option_id").get_attribute("aria-label")
            if option not in all_dropdown_options:
                all_dropdown_options.append(option)
                self.actions(action_type="key_down")
            else:
                break
        logger.info(f"Return dropdown option list: {all_dropdown_options}")
        return all_dropdown_options

    def pay_core_enable(self):
        shop_name = self.test_data.get("shop_name")
        ops_token = os.environ["OPS_TOKEN"]
        if "team_id" not in self.test_data.keys():
            merchant = self.apis.payment_ops.get_merchants_by_name(ops_token, shop_name)
            team_id = merchant["data"]["teams"]["nodes"][0].get("id")
        else:
            team_id = self.test_data["team_id"]

        support_token = os.environ.get("SUPPORT_TOKEN")
        return self.apis.payment.pay_core_enable(team_id=team_id, support_token=support_token)

    def get_inbound(self, payment_id: str, type_ops: str = "onchain_inbound"):
        ops_token = os.environ["OPS_TOKEN"]
        pay_core_enable = str(self.pay_core_enable()).lower()

        return self.apis.payment_ops.get_onchain_inbound(
            token=ops_token, payment_id=payment_id, pay_core_enable=pay_core_enable, type_ops=type_ops
        )

    def select_target_account(self, account_name: str):
        self.get_element("current_shop").actions_by_el("hover_click")
        account_list = self.get_element("account_list").web_elements

        for x in account_list:
            if x.text == account_name:
                x.click()
                break

    def verify_slack_channel_message(self, verify_type, message_type, slack_message):
        if message_type == "new_partner":
            business_role = self.test_data["business_role"]
            shop_name = self.test_data["shop_name"]
            team_id = self.test_data["team_id"]
            if business_role == "merchant":
                business_role = "Merchant"
            else:
                business_role = "Channel Partner"
            monthly_payout = "n/a"
            daily_volume_range = self.test_data.get("daily_volume_range", None)
            if daily_volume_range is None:
                annual_volume = "< 10000 USD"
            else:
                min = daily_volume_range["min"]
                max = daily_volume_range["max"]
                annual_volume = f"{min} - {max} USD"

            expected_merchant_id = f"Merchant ID: {team_id}"
            expected_merchant_name = f"Merchant Name: {shop_name}"
            expected_business_role = f"Role: {business_role}"
            expected_annual_volume = f"Annual Volume: {annual_volume}"
            expected_monthly_payout = f"Monthly Payout: {monthly_payout}"

            base_log = (
                f"【Verify if Merchant ID info is correct in slack message】Expected: {expected_merchant_id}, "
                f"Actual: {slack_message}"
            )
            if verify_type == "see":
                assert expected_merchant_id in slack_message, base_log
            else:
                assert expected_merchant_id not in slack_message, base_log

            base_log = (
                f"【Verify if Merchant Name info is correct in slack message】Expected: {expected_merchant_name},"
                f" Actual: {slack_message}"
            )
            if verify_type == "see":
                assert expected_merchant_name in slack_message, base_log
            else:
                assert expected_merchant_name not in slack_message, base_log

            base_log = (
                f"【Verify if Business Role info is correct in slack message】Expected: {expected_business_role}, "
                f"Actual: {slack_message}"
            )
            if verify_type == "see":
                assert expected_business_role in slack_message, base_log
            # else:
            #     assert expected_business_role not in slack_message, base_log

            base_log = (
                f"【Verify if Annual Volume info is correct in slack message】Expected: {expected_annual_volume}, "
                f"Actual: {slack_message}"
            )
            if verify_type == "see":
                assert expected_annual_volume in slack_message, base_log

            base_log = (
                f"【Verify if Monthly Payout info is correct in slack message】Expected: {expected_monthly_payout}, "
                f"Actual: {slack_message}"
            )
            if verify_type == "see":
                assert expected_monthly_payout in slack_message, base_log

    def get_pay_reward_rate(self):
        text = self.get_element("reward_level_text").text
        start_idx = text.find(": ") + 1
        level = text[start_idx:]

        return str(float(level.strip("%")) / 100)

    def verify_pay_reward_in_main_app(self, token: str, user_id: str, count: str = "10"):
        base_log = f"【Verify user_id {user_id} pay reward record in Main App】"
        txn_records: list = MainAppTools.get_transaction_record(token=token, count=count)
        filter_result = list(filter(lambda x: x["user_uuid"] == user_id, txn_records))
        merchant = self.test_data["shop_name"]

        if len(filter_result) == 0:
            logger.error(f"{base_log} - Not Exist")
            raise AssertionError(f"{base_log} - Not Exist")
        else:
            logger.info(f"{base_log} - Exist")

            filter_txn_type_result = list(
                filter(
                    lambda x: (
                        "pay_checkout_reward" in x["kind"] and x["meta"]["pay_checkout_reward"]["merchant"] == merchant
                    )
                    or ("crypto_payment" in x["kind"] and x["meta"]["merchant"] == merchant),
                    filter_result,
                )
            )

        base_log = f"【Verify user_id {user_id} pay reward record contains 'pay_checkout_reward' or 'crypto_payment'】"
        if len(filter_txn_type_result) == 0:
            logger.error(f"{base_log} - Failed - {filter_result}")
            raise AssertionError(f"{base_log} - Failed - {filter_result}")

        logger.info(f"{base_log} - Passed")

        reward_rate = self.test_data["reward_rate"]
        actual_reward = 0
        actual_pay = 0
        for x in filter_txn_type_result:
            if x["kind"] == "pay_checkout_reward":
                if x["amount"]["currency"] == "CRO":
                    actual_reward = abs(float(x["amount"]["amount"]))

                    get_reward_time = int(parser.parse(x["created_at"]).timestamp())
            if x["kind"] == "crypto_payment":
                if x["amount"]["currency"] == "CRO":
                    actual_pay = abs(float(x["amount"]["amount"]))

                    pay_time = int(parser.parse(x["created_at"]).timestamp())

            if actual_reward > 0 and actual_pay > 0 and (get_reward_time - pay_time <= 3600):
                actual_rate = "{0:.2f}".format(Decimal(actual_reward / actual_pay))

                base_log = f"{base_log} - Failed - reward_rate: {reward_rate}, actual_rate: {actual_rate}"
                assert actual_rate == reward_rate, base_log
                break

    def get_pay_reward_level(self):
        text = self.get_element("reward_level_text").text
        start_idx = text.find(": ") + 2
        level = text[start_idx:-2]

        return str(level.strip("%"))

    def verify_received_email(self, email_type: str, email_address: str, subject: str):
        Tools.sleep(15)
        email_address = Tools.convert_text_from_dict(str(email_address), self.test_data)
        message_content = GmailHelper().get_email_text(email_address, subject)
        if "payout" in email_type:
            shop_name = self.test_data["shop_name"]
            payout_account_currency = self.test_data["payout_account_currency"]
            payout_wallet_token = self.test_data["payout_wallet_token"]
            payout_schedule = self.test_data["payout_schedule"]
            payout_present = self.test_data.get("payout_present", None)
            payout_account_status = "APPROVED" if email_type == "payout_approved" else "REJECTED"

            error_log = f"【Verify if {shop_name} are in {email_type} email】Actual: {message_content}"
            assert shop_name in message_content, error_log

            error_log = f"【Verify if {payout_account_currency} are in {email_type} email】Actual: {message_content}"
            assert payout_account_currency in message_content, error_log

            error_log = f"【Verify if {payout_wallet_token} are in {email_type} email】Actual: {message_content}"
            assert payout_wallet_token in message_content, error_log

            error_log = f"【Verify if {payout_schedule} are in {email_type} email】Actual: {message_content}"
            assert payout_schedule in message_content, error_log

            error_log = f"【Verify if {payout_account_status} are in {email_type} email】Actual: {message_content}"
            assert payout_account_status in message_content, error_log

            if payout_schedule.lower() != "manual":
                error_log = f"【Verify if {payout_present} are in {email_type} email】Actual: {message_content}"
                assert payout_present in message_content, error_log

    def verify_email_receive(self, receive_type: str, subject: str, email: str):
        Tools.sleep(15)
        email = Tools.convert_text_from_dict(str(email), self.test_data)
        flag, e = GmailHelper().check_receive_or_not(email, subject)
        if receive_type == "success" and flag:
            logger.info(
                "Receive email - " + receive_type + " : Passed. Email : " + email + " , email subject :" + subject
            )
        elif receive_type == "failed" and (not flag):
            logger.info(
                "Receive email - " + receive_type + " : Passed. Email : " + email + " , email subject :" + subject
            )
        else:
            ops_receive = "Success" if receive_type == "failed" else "Failed"
            error = (
                "Receive email - "
                + receive_type
                + " : Failed. It expect to receive "
                + receive_type
                + ", But it received "
                + ops_receive
                + ". Email : "
                + email
                + " , email subject :"
                + subject
            )
            raise AssertionError(error)


class OpsCommonPage(BasePage):
    def __init__(self, common_page: CommonPage, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_name = "ops_common"
        self.common_page = common_page

    def navigate_to_ops(self, ops_url: str, ops_token: str = None):
        # Navigate to the ops admin page, will add token to the local storage of the browser
        # Skip the login
        if ops_token is None:
            ops_token = os.environ["OPS_TOKEN"]
        ops_url = Tools.convert_text_from_dict(ops_url, self.test_data)
        self.driver.get(ops_url)
        script = f"window.localStorage.setItem('token','{ops_token}');"
        self.driver.execute_script(script)
        self.driver.get(ops_url)
        Tools.sleep(3)

    def search_and_click_first_row(self, value: str):
        self.common_page.search_item_by(value)
        self.get_element("first_row", "common").click()

    def click_inbound_onchain_txn_link(self, payment_id: str, explorer: str = "goerli.etherscan"):
        self.search_and_click_first_row(payment_id)
        self.get_element("onchain_inbound_fund_title").wait_el(timeout=2)
        onchain_inbound_fund_txn_link = self.get_element("onchain_inbound_fund_txn_link").click()
        onchain_inbound_fund_txn = onchain_inbound_fund_txn_link.get_attribute(attr_name="href")

        txn_id = Tools.match_text_by_re(
            pattern=r"tx\/(.*)", text=onchain_inbound_fund_txn, re_type="search", first_groups=True
        )
        self.test_data["onchain_inbound_fund_txn_id"] = txn_id
        self.switch_to_windows(action="next")
        self.common_page.verify_we_are_at_correct_explorer(explorer)
        self.switch_to_windows(action="default")

    def search_and_click_sub_merchant_detail(self, value: str):
        self.common_page.search_item_by(value)
        self.get_element("first_row_detail_link").click()

    def verify_ops_sub_merchant(self, business_industry: str, mcc_code: str):
        self.assert_text("equals", self.get_element("business_industry_value").wait_el(), business_industry)
        self.assert_text("equals", self.get_element("mcc_code"), mcc_code)

    def ops_change_business_industry(self, business_industry: str):
        self.driver.execute_script("window.scrollBy(0,1000)")
        self.get_element("business_industry_dropdown").wait_el(timeout=1).actions_by_el("hover_click")
        self.test_data["currency_text"] = business_industry
        currency_item = self.get_element("currency_item", "invoices")
        currency_item.select_react_option()
        self.get_element("setting_business_save_btn", "settings").click()

        ops_token = os.environ.get("OPS_TOKEN")
        mcc_code_list = self.apis.subscriptions_ops.get_sub_merchant_mcc_code(ops_token)
        mcc_code_list = list(filter(lambda x: x["desc"] == business_industry, mcc_code_list))
        mcc_code = mcc_code_list[0]["code"]

        self.verify_ops_sub_merchant(business_industry, mcc_code)
        self.test_data["business_industry"] = business_industry

    def ops_verify_some_business_industry_were_removed(self):
        mcc_removed_list = self.test_data["mcc_removed_list"]
        for mcc_text in mcc_removed_list:
            ops_token = os.environ.get("OPS_TOKEN")
            mcc_code_list = self.apis.subscriptions_ops.get_sub_merchant_mcc_code(ops_token)
            mcc_code_list = list(filter(lambda x: x["desc"] == mcc_text, mcc_code_list))

            if len(mcc_code_list) > 0:
                logger.error(f"【Verify {mcc_text} was not removed in ops page】- Failed")
                raise AssertionError(f"【Verify {mcc_text} was not removed in ops page】- Failed")

        logger.info("【Verify some business industry were removed in ops page】- Passed")

    def search_and_verify_text_by_td_index(self, value: str, index: int, expected_text):
        self.common_page.search_item_by(input_value=value)
        self.test_data["first_row_td_index"] = index
        actual_text = self.get_element("text_by_td_index_first_row").text
        actual_text_log = (
            f"【Verify expected text in table {index} td of {self.driver.current_url}】: "
            f"Actual {actual_text}, Expected {expected_text}"
        )
        assert actual_text == expected_text, actual_text_log
        logger.info(f"{actual_text_log} - Passed")

    def ops_business_role_dropdown_change(self, role_type: str):
        self.get_element("business_role_dropdown").click()
        a_or_m = Tools.convert_text_from_dict(role_type, self.test_data)
        self.test_data["business_role"] = a_or_m
        self.get_element("business_role_item").click()
        self.get_element("save_btn").click()
        Tools.sleep(3)

    def ops_change_business_owner(self, add_type: str, cancel=False, auto_complete=False, required_check=False):
        self.navigate_to_ops("<global_ops_host>/merchant_details/<team_id>")
        business_owner_first_name_value = self.get_element("business_owner_first_name_value")
        business_owner_last_name_value = self.get_element("business_owner_last_name_value")
        business_owner_first_name_text = None
        business_owner_last_name_text = None
        check_business_owner_first_name_value = self.check_el_execute(business_owner_first_name_value, True)
        if check_business_owner_first_name_value:
            if len(business_owner_first_name_value.web_elements) > 1:
                self.test_data["index"] = len(business_owner_first_name_value.web_elements)
                business_owner_first_name_value = self.get_element("business_owner_first_name_item")
                business_owner_last_name_value = self.get_element("business_owner_last_name_item")
            business_owner_first_name_text = business_owner_first_name_value.text
            business_owner_last_name_text = business_owner_last_name_value.text

        business_type = None
        edd_flag = False
        if ":" in add_type:
            business_type = add_type.split(":")[1]
            add_type = add_type.split(":")[0]
            if "_edd" in business_type:
                edd_flag = True
                business_type = business_type.split("_")[0]

        if edd_flag:
            set_edd_checkbox_enabled = self.check_el_execute(self.get_element("set_edd_checkbox_enabled"), True)
            if not set_edd_checkbox_enabled:
                self.get_element("set_edd_checkbox").click()
                save_btn = self.get_element("save_btn")
                if self.check_el_execute(save_btn, True):
                    save_btn.click()

        if add_type == "edit":
            self.get_element("business_owner_edit_btn").click()
        else:
            self.get_element("business_owner_add_btn").click()
        self.get_element("business_owner_title").assert_object("see")
        time_str = datetime.now().strftime("%Y%m%d%H%M%S%f")
        first_name = f"firstName{time_str}"
        last_name = f"lastName{time_str}"
        first_name_field = self.get_element("business_repr_first_name", "settings")
        last_name_field = self.get_element("business_repr_last_name", "settings")
        date_of_birth_field = self.get_element("business_repr_dob", "settings")
        if required_check:
            if add_type == "edit":
                first_name_field.clear_input_field(clear_count=2)
                last_name_field.clear_input_field(clear_count=2)
                self.get_element("business_owner_date_of_birth_clear_btn").actions_by_el("hover_click")
            self.get_element("ok_btn", "settings").click()
            self.get_element("business_owner_first_name_alert").assert_object("see")
            self.get_element("business_owner_last_name_alert").assert_object("see")
            self.get_element("business_owner_date_of_birth_alert").assert_object("see")
            if add_type != "edit":
                self.get_element("business_owner_nationality_alert").assert_object("see")

            field_list = ["First Name", "Last Name", "Date of Birth", "Nationality"]
            if add_type == "add":
                field_list.append("or Auto-complete from User Profile")
            for label_name in field_list:
                self.test_data["label_name"] = label_name
                self.get_element("business_owner_title_name").assert_object("see")

            self.get_element("cancel_btn", "settings").click()

        else:
            if not auto_complete:
                first_name_field.input(first_name, clear=True, clear_count=2)
                last_name_field.input(last_name, clear=True, clear_count=2)
            else:
                self.get_element("auto_complete_business_owner_dropdown").click()
                self.get_element("auto_complete_user_profile_item", "settings").wait_el(timeout=1).click()
            date_of_birth_field.input(datetime.now().strftime("%d/%m/%Y"), enter=True)
            self.get_element("business_repr_nation", "settings").input("Afghanistan", enter=True)
            if not cancel or auto_complete:
                current_first_name = first_name_field.text
                current_last_name = last_name_field.text
                self.get_element("ok_btn", "settings").click()
                Tools.sleep(1)
            else:
                current_first_name = business_owner_first_name_text
                current_last_name = business_owner_last_name_text
                self.get_element("cancel_btn", "settings").click()

            business_owner_first_name_value = self.get_element("business_owner_first_name_value")
            if len(business_owner_first_name_value.web_elements) > 1:
                self.test_data["index"] = len(business_owner_first_name_value.web_elements)
                business_owner_first_name_value = self.get_element("business_owner_first_name_item")
                business_owner_last_name_value = self.get_element("business_owner_last_name_item")
                business_owner_first_name_dashboard = self.get_element(
                    "business_owner_first_name_dashboard_item", "settings"
                )
                business_owner_last_name_dashboard = self.get_element(
                    "business_owner_last_name_dashboard_item", "settings"
                )
            else:
                business_owner_first_name_dashboard = self.get_element("business_owner_first_name", "settings")
                business_owner_last_name_dashboard = self.get_element("business_owner_last_name", "settings")

            business_owner_first_name_value.wait_el(timeout=1).assert_text("equals", current_first_name)
            business_owner_last_name_value.wait_el(timeout=1).assert_text("equals", current_last_name)

            if business_type == "individual":
                self.common_page.navigate_to_url("<global_host>/settings/business")
                self.get_element("business_owners_link", "settings").assert_object("notsee")
            else:
                self.common_page.navigate_to_url("<global_host>/settings/business/business-owner")
                business_owner_first_name_dashboard.assert_text("equals", current_first_name)
                business_owner_last_name_dashboard.assert_text("equals", current_last_name)

    def set_configuration(self, data_set: str):
        configurations_field = self.get_element("configurations_field")

        if not self.test_data[data_set]:
            raise ValueError(f"【Get {data_set} data failed in test data】")

        data = json.dumps(self.test_data[data_set])
        configurations_field.input(data, clear=True, clear_count=2)
        self.click_save_btn()

    def search_and_double_click_first_row(self, value: str):
        self.common_page.search_item_by(value)
        self.get_element("first_payout_row", "common").actions_by_el("double_click")
        Tools.sleep(1)

    def verify_payout_details_currency(self, balance: str, currency: str):
        self.test_data["balance_text"] = balance
        self.test_data["currency_text"] = currency

        self.get_element("payout_details_title_amount_currency").assert_object("see")
        self.get_element("payout_details_amount_currency").assert_object("see")
        self.get_element("payout_details_fee_currency").assert_object("see")

        payout_details_currency = self.get_element("payout_details_currency")
        base_log = f"【Verify ops payout_details Fee currency failed 】E: {balance}, A: {payout_details_currency.text}"
        assert payout_details_currency.text == currency, base_log

    def click_save_btn(self):
        check_status = True
        while check_status:
            self.get_element("save_btn").click()
            server_busy_message = self.get_element("server_busy_message")
            check_server_busy_message = self.check_el_execute(server_busy_message, True)
            if check_server_busy_message:
                self.get_element("error_close_btn").click()
                Tools.sleep(5)
            else:
                check_status = False
