import logging
import time
from typing import List, Union, Optional

from cdc.qa.pageobject.locator import SelectorLocator
from cdc.qa.pageobject.element import Element
from selenium.webdriver import ActionChains
from appium.webdriver.webdriver import WebDriver as MobileDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from ..page import Page

from selenium.webdriver.common.keys import Keys

logger = logging.getLogger(__name__)


class SuperElement(Element):
    def __init__(
        self,
        locator_name: str,
        locator: SelectorLocator = None,
        page: Page = None,
    ):
        super().__init__(locator, page)
        self.base_page = page
        self.locator_name = locator_name
        self.find_by = f"< {locator.by}: {locator.value} >"
        self.external_locator: List[SelectorLocator] = list()

    def get_element(self):
        return self._web_element

    @property
    def web_elements(self):
        els = self.base_page.driver.find_elements(by=self.locator.by, value=self.locator.value)
        if len(els) > 0:
            return els

        if len(self.external_locator) > 0:
            for s in self.external_locator:
                self.find_by = f"< {s.by}: {s.value} >"
                els = self.base_page.driver.find_elements(by=s.by, value=s.value)
                if len(els) > 0:
                    return els
                else:
                    logger.debug(f"【Find {self.locator_name} by external locator FAILED】: -> {self.find_by}")
        raise Exception(f"【Elements {self.locator_name} not found】: -> {self.find_by}")

    @property
    def _web_element(self):
        el = None
        last_e = None
        found = False

        try:
            el = self.base_page.driver.find_element(by=self.locator.by, value=self.locator.value)
            found = True
        except Exception as e:
            last_e = e
            logger.debug(f"【Find {self.locator_name} by first locator FAILED】: {str(e.__getattribute__('msg'))}")

        if len(self.external_locator) > 0 and not found:
            for s in self.external_locator:
                self.find_by = f"< {s.by}: {s.value} >"
                try:
                    el = self.base_page.driver.find_element(by=s.by, value=s.value)
                    found = True
                    break
                except Exception as e:
                    logger.debug(f"【Find {self.locator_name} by external locator FAILED】: -> {self.find_by}")
                    last_e = e

        if not found:
            raise last_e
        return el

    def input(self, value: Union[str, int, float], clear: bool = False, enter: bool = False, clear_count: int = 1):
        try:
            value = str(value)
            value = convert_text_from_dict(value, self.base_page.test_data)
            if clear:
                self.clear_input_field(clear_count)
            if enter:
                self._web_element.send_keys(value, Keys.ENTER)
            else:
                self._web_element.send_keys(value)

            logger.debug(f"【Input on {self.locator_name} with text {value}】-> Find by {self.find_by}")
            return self
        except Exception as e:
            error_msg = f"【Input FAILED on {self.locator_name}】-> Find by {self.find_by}"
            logger.error(error_msg)
            raise exception_msg(e, error_msg)

    def clear_input_field(self, clear_count: int = 1):
        try:
            for i in range(clear_count):
                chars = self._web_element.text
                if chars == "":
                    chars = self._web_element.get_attribute("value")

                self._web_element.click()
                if chars != "":
                    for c in chars:
                        self._web_element.send_keys(Keys.BACKSPACE)
                else:
                    break
        except Exception as e:
            error_msg = f"【Clear input field FAILED on {self.locator_name}】-> Find by {self.find_by}"
            logger.error(error_msg)
            raise exception_msg(e, error_msg)

    def input_key(self, key: str):
        """Need update the Mobile Key code or rebuild this function"""
        try:
            if key == "enter":
                key = Keys.ENTER
            elif key == "backspace" or key == "back_space":
                key = Keys.BACKSPACE
            elif key == "tab":
                key = Keys.TAB
            elif key == "ctl_a":
                key = Keys.CONTROL + "a"
            elif key == "command_a":
                key = Keys.COMMAND + "a"
            else:
                raise ValueError(f"Not implemented error key: '{key}'.")
            self._web_element.send_keys(key)

            logger.debug(f"【Input on {self.locator_name} with key {key}】-> Find by {self.find_by}")
            return self

        except Exception as e:
            error_msg = f"【Input key FAILED on {self.locator_name}】-> Find by {self.find_by}"
            logger.error(error_msg)
            raise exception_msg(e, error_msg)

    def click(self):
        try:
            self._web_element.click()
            logger.debug(f"【Click on {self.locator_name}】-> Find by {self.find_by}")
            return self
        except Exception as e:
            error_msg = f"【Click FAILED on {self.locator_name}】-> Find by {self.find_by}"
            logger.error(error_msg)
            raise exception_msg(e, error_msg)

    @property
    def text(self):
        try:
            el = self._web_element
            text = el.text
            if text == "":
                text = el.get_attribute("value")

            logger.debug(f"【Get text on {self.locator_name} with {text}】-> Find by {self.find_by}")
            return text
        except Exception as e:
            error_msg = f"【Get text FAILED on {self.locator_name}】-> Find by {self.find_by}"
            logger.error(error_msg)
            raise exception_msg(e, error_msg)

    def actions_by_el(self, action_type: str):
        """Will split the actions between actions and touch actions"""
        el = self.get_element()
        a = ActionChains(self.base_page.driver)

        if action_type == "hover":
            a.move_to_element(el).perform()
        elif action_type == "hover_click":
            a.move_to_element(el).click().perform()
        elif action_type == "double_click":
            a.move_to_element(el).double_click().perform()
        elif action_type == "scroll_to_el":
            self.page.driver.execute_script("arguments[0].scrollIntoView();", el)
        else:
            raise ValueError(f"Not implemented error actions type: '{action_type}'.")

        logger.info(f"【Execute {action_type} action on {self.locator_name}】: Find by -> {self.find_by}")
        return self

    def wait_el(self, timeout: Optional[int] = 3, action: str = "wait_first"):
        """
        Use implicit wait to wait the expected element.
        wait_first - Wait {timeout} and find element
        wait_interval - Loop to find element by interval 1 second, total {timeout}
        wait_after - Find element first and wait {timeout}
        @param timeout:  timeout
        @param action: wait_first, wait_interval and wait_after
        @return: self
        """
        last_e = None
        if action == "wait_interval":
            end_time = time.time() + timeout + 2
            while True:
                try:
                    self.get_element()
                    last_e = None
                    break
                except Exception as e:
                    last_e = e
                sleep(timeout=1)
                if time.time() > end_time:
                    break
        elif action == "wait_after":
            try:
                self.get_element()
                sleep(timeout=timeout)
            except Exception as e:
                last_e = e
        else:
            sleep(timeout=timeout)
            try:
                self.get_element()
            except Exception as e:
                last_e = e
        base_log = f"【Wait {self.locator_name} by action {action} with timeout {timeout}】"
        if last_e is not None:
            error_msg = f"{base_log} - FAILED -> Find by {self.find_by}"
            logger.error(error_msg)
            raise exception_msg(last_e, error_msg)
        else:
            logger.info(f"{base_log} - PASSED -> Find by {self.find_by}")
            return self

    def select_react_option(self, loop_time: int = 20, key_down_time: int = 2):
        """Web only"""
        if isinstance(self.base_page.driver, MobileDriver):
            raise ValueError("Function select_react_option web only")

        is_succeed = False
        for i in range(loop_time):
            check_select_item, select_item = self.ec_wait(timeout=1)
            if check_select_item:
                self.click()
                is_succeed = True
                break
            else:
                a = ActionChains(self.base_page.driver)
                for k in range(key_down_time):
                    a.key_down(Keys.DOWN).perform()

        if is_succeed:
            logger.info(f"【Select react option PASSED】: Find by -> {self.find_by}")
        else:
            logger.error(f"【Select react option FAILED after loop {loop_time} times】: Find by -> {self.find_by}")

    def get_attribute(self, attr_name: str = "value"):
        try:
            attr_value = self._web_element.get_attribute(attr_name)
            if attr_value == "" or attr_value is None:
                error_msg = (
                    f"【None any attribute value for "
                    f"{self.locator_name} by attr name {attr_name}】-> Find by {self.find_by}"
                )
                logger.error(error_msg)
                raise Exception(error_msg)

            logger.info(
                f"【Get element attribute PASSED on "
                f"{self.locator_name} by attr name {attr_name}】-> Find by {self.find_by}"
            )
            return attr_value
        except Exception as e:
            error_msg = (
                f"【Get element attribute FAILED on "
                f"{self.locator_name} by attr name {attr_name}】-> Find by {self.find_by}"
            )
            logger.error(error_msg)
            raise exception_msg(e, error_msg)

    def ec_wait(
        self,
        action_type: str = "visibility",
        condition_result: bool = True,
        timeout: int = 3,
        poll_time=0.5,
        message: str = None,
        ignored_exceptions=True,
        **condition_params,
    ):
        """Use Explicit Waits to check if the element exist or other condition found

        Args:
            action_type (str, optional): action type,
                    allow:visibility, presence, title_contains, title_is, contains_text, clickable.
                    Defaults to "visibility".
            condition_result (bool, optional): condition result. Defaults to True.
            timeout (int, optional): timeout seconds. Defaults to 3.
            poll_time (float, optional): poll time seconds. Defaults to 0.5.
            message (str, optional): message. Defaults to None.
            ignored_exceptions: raise exceptions or not
        Raises:
            ValueError: no action type implement
            Exception: raise EC failed exception when ignored_exceptions False

        Returns:
            (bool, self): return EC result and element self
        """
        ec_wait = WebDriverWait(driver=self.page.driver, timeout=timeout, poll_frequency=poll_time)
        if condition_result:
            wait_method = ec_wait.until
        else:
            wait_method = ec_wait.until_not
        locator = (self.locator.by, self.locator.value)

        if action_type == "visibility":
            ec_condition = ec.visibility_of_element_located(locator)
        elif action_type == "presence":
            ec_condition = ec.presence_of_element_located(locator)
        elif action_type == "title_contains":
            ec_condition = ec.title_contains(title=condition_params["title"])
        elif action_type == "title_is":
            ec_condition = ec.title_is(title=condition_params["title"])
        elif action_type == "contains_text":
            ec_condition = ec.text_to_be_present_in_element(locator=locator, text_=condition_params["text_"])
        elif action_type == "clickable":
            ec_condition = ec.element_to_be_clickable(locator)
        else:
            raise ValueError(f"Not implemented error action: '{action_type}'.")

        self.page.driver.implicitly_wait(0)
        base_msg = f"EC wait {self.locator_name} {action_type}"
        success = False
        try:
            wait_method(ec_condition, message=message)
            success = True
        except Exception as e:
            logger.debug(f"{base_msg} by first locator FAILED: -> Find by {self.find_by} Error:{str(e)}")

        locator_actions = ["visibility", "presence", "contains_text", "clickable"]
        if success is False and action_type in locator_actions and len(self.external_locator) > 0:
            for s in self.external_locator:
                self.find_by = f"< {s.by}: {s.value} >"
                try:
                    ec_condition.locator = (s.by, s.value)
                    wait_method(ec_condition, message=message)
                    success = True
                    break
                except Exception as e:
                    logger.debug(f"{base_msg} by external locator FAILED: -> Find by {self.find_by} Error:{str(e)}")

        self.page.driver.implicitly_wait(8)
        logger.info(f"{base_msg} {'PASSED' if success else 'FAILED'}: -> Find by {self.find_by}")

        if success:
            return success, self
        else:
            if ignored_exceptions:
                return success, self
            else:
                raise Exception(f"{base_msg} FAILED!")

    def assert_object(self, asset_type: str):
        """
        Asset the element in page if see or not see
        @param asset_type: see or notsee
        """
        verify_status = False
        last_e = None
        base_log = f"【Verify object {self.locator_name} if {asset_type} 】: "

        try:
            self.get_element()
            if asset_type == "see":
                verify_status = True
        except Exception as e:
            last_e = e
            if asset_type == "notsee":
                verify_status = True

        if verify_status:
            logger.info(f"{base_log} Find by -> {self.find_by} - PASSED")
            return self
        else:
            error = f"{base_log} Find by -> {self.find_by} - FAILED: {str(last_e)}"
            logger.error(error)
            raise exception_msg(last_e, error)

    def assert_text(self, assert_type: str, expected_text: str):
        """
        Assert element text if equals, notequals, contains or notcontains the expected text
        @param assert_type: equals, notequals, contains or notcontains
        @param expected_text:expected_text
        """
        last_e = None
        verify_status = False
        base_log = f"【Verify object {self.locator_name} text if {assert_type} to】"
        expected_text = convert_text_from_dict(str(expected_text), self.base_page.test_data)

        try:
            actual_text = self.text
            base_log = f"{base_log} Actual is: {actual_text}, Expected is: {expected_text}, Find by -> {self.find_by}"
            if assert_type == "contains" and expected_text in actual_text:
                verify_status = True
            if assert_type == "notcontains" and expected_text not in actual_text:
                verify_status = True
            if assert_type == "equals" and expected_text == actual_text:
                verify_status = True
            if assert_type == "notequals" and expected_text != actual_text:
                verify_status = True
        except Exception as e:
            last_e = e

        if verify_status:
            logger.info(f"{base_log} - PASSED")
            return self
        elif last_e is None:
            raise Exception(base_log + "- FAILED")
        else:
            error = f"{base_log} - FAILED: {str(last_e)}"
            logger.error(error)
            raise exception_msg(last_e, error)


def convert_text_from_dict(text: str, data: dict):
    """
    Replace all '<.*>' in text
    example: submit_btn = //button[.='<button_text>'], data = {"button_text": "Submit"}
    submit_btn = convert_text_from_dict(submit_btn, data)
    submit_btn = "//button[.='Submit']
    @param text: text need to convert
    @param data: a map store all possible values can be converted
    @return: converted text
    """
    import re

    r = re.compile("[<>]+").findall(text)
    if len(r) == 0:
        return text

    r = re.compile("(<.*?>)").findall(text)
    keys = data.keys()

    for v in r:
        key = v.replace("<", "").replace(">", "")
        if key in keys:
            after = str(data[key])
            text = text.replace(v, after)

    return text


def exception_msg(e: BaseException, msg: str):
    if e is not None:
        e_msg = e.__getattribute__("msg")
        msg = f"{msg}: {e_msg}"
    else:
        e = Exception(msg)
    e.__setattr__("msg", msg)
    return e


def sleep(timeout: int = 1, sleep_type: str = "event"):
    from threading import Event

    if sleep_type == "event":
        e = Event()
        e.wait(timeout=timeout)
    else:
        end_time = time.time() + timeout
        while True:
            if time.time() > end_time:
                break
