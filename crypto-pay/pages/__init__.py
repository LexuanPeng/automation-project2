from common.api import Apis
from pages.common_page import CommonPage, OpsCommonPage
from pages.login_page import LoginPage
from pages.staging.web import Pages as StgWebPages


class SuperPages:
    def __init__(self, *args, **kwargs):
        self.common_page = CommonPage(*args, **kwargs)
        self.ops_common_page = OpsCommonPage(self.common_page, *args, **kwargs)
        self.login_page = LoginPage(self.common_page, *args, **kwargs)
        self.staging_web_pages = StgWebPages(self.common_page, self.ops_common_page, self.login_page, *args, **kwargs)
        self.test_data: dict = kwargs.get("test_data", None)
        self.apis: Apis = kwargs.get("apis", None)
