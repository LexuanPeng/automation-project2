from __future__ import annotations
from typing import TypeVar
from abc import abstractmethod

from appium.webdriver.common.touch_action import TouchAction

from .element import Element
from ....locator import SelectorLocator, PositionLocator
from ....common.coordinate import Coordinate

import logging

T = TypeVar("T", bound="ButtonElement")

logger = logging.getLogger(__name__)


class ButtonElement(Element):
    def click(self: T, raw_click: bool = False) -> T:
        def _click_with_coordinate(coordinate: Coordinate):
            logger.debug(f"Click with coordinate: x={coordinate.x}, y={coordinate.y}")
            TouchAction(self.page.driver).tap(x=int(coordinate.x), y=int(coordinate.y)).perform()

        if isinstance(self.locator, SelectorLocator):
            if raw_click:
                _click_with_coordinate(self.center)
            else:
                logger.debug(f"Click element: {self}")
                self._web_element.click()

        elif isinstance(self.locator, PositionLocator):
            _click_with_coordinate(self.center)

        else:
            raise ValueError

        return self

    @staticmethod
    @abstractmethod
    def _long_press_touch_action(driver, time_in_ms, **kwargs):
        pass

    def long_press(self: T, time_in_second: int = 2, raw_click: bool = False) -> T:
        time_in_ms = time_in_second * 1000

        def _long_press_with_coordinate(coordinate: Coordinate):
            logger.debug(f"Long press with coordinate for {time_in_second} seconds: x={coordinate.x}, y={coordinate.y}")
            self._long_press_touch_action(self.page.driver, time_in_ms, x=int(coordinate.x), y=int(coordinate.y))
            TouchAction().long_press().wait(ms=time_in_ms).release().perform()

        if isinstance(self.locator, SelectorLocator):
            if raw_click:
                _long_press_with_coordinate(self.center)
            else:
                logger.debug(f"Long press on element for {time_in_second} seconds: {self}")
                self._long_press_touch_action(self.page.driver, time_in_ms, el=self._web_element)

        elif isinstance(self.locator, PositionLocator):
            _long_press_with_coordinate(self.center)

        else:
            raise ValueError

        return self
