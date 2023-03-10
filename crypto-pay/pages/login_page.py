import datetime
import logging

from common.utils.tools import ImapEmail, Tools
from pages.base_page import BasePage
from pages.common_page import CommonPage

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    def __init__(self, common_page: CommonPage, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.common_page = common_page
        self.page_name = "login"

        # 导航到登录页面

    def navigate_to_login_home(self, url: str):
        # Navigate to login home page and verify login form objects exist
        self.common_page.navigate_to_url(url)
        self.get_element("login_field").wait_el(timeout=3)
        self.get_element("password_field").assert_object("see")
        self.get_element("sign_in_btn").assert_object("see")

    def login_by_user_pwd(self, user_name: str, password: str):
        self.input_user_pwd(user_name=user_name, password=password)

        # self.get_element("user_link", "common").wait_el(timeout=3, action="wait_first")
        logger.info(f"【Login by user and password】: {user_name} - {password}")
        Tools.sleep(3)

    def input_user_pwd(self, user_name: str, password: str):
        # Login by user_name and password
        self.get_element("geetest_btn").wait_el(timeout=3).click()
        user_name = Tools.convert_text_from_dict(user_name, self.test_data)
        password = Tools.convert_text_from_dict(password, self.test_data)
        self.get_element("login_field").input(user_name, clear=True, clear_count=2)
        self.get_element("password_field").input(password, clear=True, clear_count=2)

        self.get_element("sign_in_btn").wait_el(timeout=1).click()

    def verify_success_after_login(self):
        # Verify login form objects not exist after login success
        self.assert_object("notsee", self.get_element("login_field"))
        self.assert_object("notsee", self.get_element("password_field"))
        # Verify we redirect to home page after login success
        self.test_data["main_title"] = "Overview"
        self.assert_text("equals", self.get_element(name="main_title", page="common"), "Overview")