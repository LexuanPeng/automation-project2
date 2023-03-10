from __future__ import annotations
import yaml
import logging
from typing import TYPE_CHECKING

from common.api import Apis
from cdc.qa.pageobject.element.super import SuperElement
from cdc.qa.pageobject.locator import SelectorLocator
from cdc.qa.pageobject.page import WebPage
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from common.utils.tools import Tools
import base64

base64.encodestring = base64.encodebytes

if TYPE_CHECKING: # type_checking的作用是指不会真正导入下列模块，但是能起到提示作用
    from cdc.qa.core import WebApp, WebDevice

logger = logging.getLogger(__name__)


# 初始化数据
class BasePage(WebPage):
    def __init__(
        self,
        driver: WebDriver,
        device: WebDevice,
        env: str = "staging",
        test_data: dict = None,
        app: WebApp = None,
        page_name: str = None,
        apis: Apis = None,
    ):
        super().__init__(app, device, driver)
        self.device = device
        self.driver = driver
        self.test_data = test_data
        self.env = env
        self.page_name = page_name
        self.apis = apis

    @staticmethod
    def assert_object(asset_type: str, es: SuperElement):
        """Move this function into super"""
        return es.assert_object(asset_type=asset_type)

    @staticmethod
    def assert_text(assert_type: str, es: SuperElement, expected_text: str):
        """Move this function into super"""
        return es.assert_text(assert_type=assert_type, expected_text=expected_text)

    def get_element(self, name: str, page: str = None) -> SuperElement:
        """
        Get the element by page, If not provide page name, it will set the ***Page to default
        @param name: element name in yaml
        @param page: element page of yaml file name
        @return: SuperElement
        """
        if page is None:
            page = self.page_name

        # 通过yaml文件获取元素定位器及值
        ops: dict = yaml.safe_load(open(f"test_resource/objects/{self.env}/{page}_page.yaml"))
        if name not in ops.keys():
            raise ValueError(f"【Test object {name} not found in {self.env}/{page}_page.yaml】")

        op = ops[name]
        if isinstance(op, list):
            super_element = None
            for ee in op:
                # Always set the first one to main super element
                for k, v in ee.items():
                    v = Tools.convert_text_from_dict(v, self.test_data)
                    s = SelectorLocator(k, v)
                    if super_element is None:
                        super_element = SuperElement(name, s, self)
                    else:
                        super_element.external_locator.append(s)
            return super_element
        else:
            for k, v in op.items():
                v = Tools.convert_text_from_dict(v, self.test_data)
                s = SelectorLocator(k, v)
                super_element = SuperElement(name, s, self)
                return super_element

    @staticmethod
    def check_el_execute(es: SuperElement, exist: bool = True, verify_display: bool = True) -> bool:
        """
        Check the element if exist or not exist and then return True not False
        @param verify_display: To check if the element dom is displayed
        @param es: SuperElement
        @param exist: exist or not exist
        @return: True not False
        """
        base_log = f"【Check if element {es.locator_name} exist {exist} and execute】: "
        if exist:
            try:
                el = es.get_element()

                if not verify_display:
                    return True

                if el.is_displayed():
                    logger.info(f"{base_log} Find by -> {es.find_by}")
                    return True
                else:
                    logger.debug(f"{base_log} But element not display, Find by -> {es.find_by}")
                    return False

            except Exception as e:
                logger.debug(
                    f"{base_log} But element not exist, Find by -> {es.find_by} - {str(e.__getattribute__('msg'))}"
                )
                return False
        else:
            try:
                el = es.get_element()

                if not el.is_displayed():
                    logger.info(f"{base_log} Find by -> {es.find_by}")
                    return True
                logger.debug(f"{base_log} But element exist, Find by -> {es.find_by}")
                return False

            except Exception as e:
                logger.debug("Ignore msg: " + str(e))
                logger.info(f"{base_log} Find by -> {es.find_by}")
                return True

    def actions(self, action_type: str, x: float = None, y: float = None):
        """
        Mouse action or keyboard action on current page, but not using SupperElement
        @param action_type:  please see below code
        @param x: x, default is None
        @param y: y, default is None
        """
        a = ActionChains(self.driver)

        if action_type == "hover":
            a.move_by_offset(x, y).perform()
        elif action_type == "hover_click":
            a.move_by_offset(x, y).click().perform()
        elif action_type == "double_click":
            a.move_by_offset(x, y).double_click().perform()
        elif action_type == "key_down":
            a.key_down(Keys.DOWN).perform()
        elif action_type == "key_up":
            a.key_down(Keys.UP).perform()
        elif action_type == "esc":
            a.key_down(Keys.ESCAPE).perform()
        elif action_type == "enter":
            a.key_down(Keys.ENTER).perform()
        else:
            raise ValueError(f"Not implemented error actions type: '{action_type}'.")

        logger.info(f"【Execute {action_type} action】")

    def switch_to_windows(self, action: str = "next", window: str = None):
        """Switch to windows"""
        window_handles: list = self.driver.window_handles
        if len(window_handles) == 1:
            current_window_handle = self.driver.current_window_handle
            logger.info(f"【Current browser has no extra windows】: {window_handles}")
            return self.driver.switch_to.window(current_window_handle)

        if action == "next":
            window = window_handles[1]
            self.driver.switch_to.window(window)
        elif action == "expect":
            self.driver.switch_to.window(window)
        elif action == "default":
            window = window_handles[0]
            self.driver.switch_to.window(window)
        elif action == "third":
            window = window_handles[2]
            self.driver.switch_to.window(window)
        elif action == "fourth":
            window = window_handles[3]
            self.driver.switch_to.window(window)
        elif action == "fifth":
            window = window_handles[4]
            self.driver.switch_to.window(window)
        elif action == "sixth":
            window = window_handles[5]
            self.driver.switch_to.window(window)
        elif action == "seventh":
            window = window_handles[6]
            self.driver.switch_to.window(window)
        elif action == "eighth":
            window = window_handles[7]
            self.driver.switch_to.window(window)
        else:
            raise NotImplementedError("Not implemented action for switch to windows")
        logger.info(f"【Switch to {action} windows {window}】: {self.driver.title}")

    def switch_to_parent_frame(self):
        return self.driver.switch_to.parent_frame()

    def switch_to_frame(self, frame_name):
        frame_name = self.get_element(frame_name).wait_el(timeout=20, action="wait_interval")
        return self.driver.switch_to.frame(frame_name._web_element)

    def click_element_javascript(self, ele):
        element = self.get_element(ele).get_element()
        self.driver.execute_script("arguments[0].click();", element)
        logger.info(f"javascript click {ele} success")

    def select_element_javascript(self, ele, item):
        element = self.get_element(ele).get_element()
        try:
            self.driver.execute_script(
                "const textToFind = '"
                + item
                + "';"
                + "const dd = arguments[0];"
                + "dd.selectedIndex = [...dd.options].findIndex (option => option.text === textToFind);",
                element,
            )
            logger.info(f"javascript select {ele} by {item} success")
        except Exception as e:
            raise e
