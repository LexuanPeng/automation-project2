from common.api import Apis
from pages.common_page import CommonPage, OpsCommonPage
from pages.login_page import LoginPage


class Pages:
    def __init__(self, common_page: CommonPage, ops_common_page: OpsCommonPage, login_page: LoginPage, *args, **kwargs):
        self.common_page = common_page
        self.ops_common_page = ops_common_page
        self.login_page = login_page
        self.test_data: dict = kwargs.get("test_data", None)
        self.apis: Apis = kwargs.get("apis", None)
