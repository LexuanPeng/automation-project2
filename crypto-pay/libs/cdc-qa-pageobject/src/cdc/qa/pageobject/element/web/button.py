from __future__ import annotations
from typing import TypeVar

from .element import Element
from ...locator import SelectorLocator, PositionLocator
from ...common.coordinate import Coordinate

from selenium.webdriver.common.action_chains import ActionChains

T = TypeVar("T", bound="ButtonElement")


class ButtonElement(Element):
    def click(self: T, raw_click: bool = False) -> T:
        def _click_with_coordinate(coordinate: Coordinate):
            ac = ActionChains(self.page.driver)
            el_body = self.page.driver.find_element_by_tag_name("body")
            ac.move_to_element_with_offset(el_body, coordinate.x, coordinate.y).click().perform()

        if isinstance(self.locator, SelectorLocator):
            if raw_click:
                _click_with_coordinate(self.center)
            else:
                self._web_element.click()

        elif isinstance(self.locator, PositionLocator):
            _click_with_coordinate(self.center)

        else:
            raise ValueError

        return self
