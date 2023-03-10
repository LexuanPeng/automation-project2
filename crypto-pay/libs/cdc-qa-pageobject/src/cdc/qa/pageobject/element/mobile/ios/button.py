from __future__ import annotations

from appium.webdriver.common.touch_action import TouchAction

from .element import Element
from ..base.button import ButtonElement as BaseButtonElement


class ButtonElement(BaseButtonElement, Element):
    @staticmethod
    def _long_press_touch_action(driver, time_in_ms, **kwargs):
        TouchAction(driver).long_press(**kwargs).wait(ms=time_in_ms).release().perform()
