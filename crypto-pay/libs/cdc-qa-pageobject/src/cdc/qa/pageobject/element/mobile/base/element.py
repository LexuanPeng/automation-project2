from __future__ import annotations

import logging
import os
from typing import Optional, TypeVar, cast

from ...element import Element as BaseElement
from ....common.exception import ElementNotFoundException
from ....common.rect import Rect
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException

T = TypeVar("T", bound="Element")

logger = logging.getLogger(__name__)

DEFAULT_SCROLL_DEADZONE = float(os.environ.get("PAGEOBJECT_DEFAULT_SCROLL_DEADZONE", 0.3))


class Element(BaseElement):
    def scroll_to(
        self: T,
        container_element: Optional[T] = None,
        timeout: Optional[int] = None,
        tries: int = 10,
        deadzone: Optional[float] = None,
        condition: Optional[EC] = None,
        direction: Optional[str] = "down",
    ) -> T:
        """Find this element by scrolling its container element.
        Args:
            container_element (element.mobile.base.Element, Optional): The element to be scrolled.
                If None, will scroll based on the whole window.
                Defaults to None.
            timeout (int, Optional): Wait timeout for each try.
                Defaults to None.
            tries (int, Optional): Number of tries on scrolling and locating the element.
                Defaults to 10.
            deadzone (float, Optional): The deadzone between scrolling on both ends.
                Defaults to None.
            condition (expected_conditions, Optional): The expected conditions of element wait.
                Defaults to None.
            directions (directions, Optional): The directions to scroll to.
                Defaults to down
        Returns:
            self
        """

        # TODO: Handle scrolling backwards to reset the container element
        # ? Consider using `UiSelector` to handle scrolling in Android for better performance

        if direction not in ["up", "down", "left", "right"]:
            raise ValueError(f"Not implemented directions, {direction}")

        if not deadzone:
            deadzone = DEFAULT_SCROLL_DEADZONE

        for _ in range(tries):
            try:
                return self.wait(timeout=timeout, condition=condition)
            except TimeoutException:
                if container_element:
                    container_rect = container_element.rect
                else:
                    window_size = self.page.driver.get_window_size()
                    container_rect = Rect(
                        x=0, y=0, width=float(window_size["width"]), height=float(window_size["height"])
                    )
                xi = xf = int(container_rect.x + container_rect.width * 0.5)
                yi = yf = int(container_rect.y + container_rect.height * 0.5)
                if direction == "down":
                    yi = int(container_rect.y + container_rect.height * (1 - deadzone))
                    yf = int(container_rect.y + container_rect.height * deadzone)
                elif direction == "up":
                    yi = int(container_rect.y + container_rect.height * deadzone)
                    yf = int(container_rect.y + container_rect.height * (1 - deadzone))
                elif direction == "left":
                    xi = int(container_rect.x + container_rect.width * deadzone)
                    xf = int(container_rect.x + container_rect.width * (1 - deadzone))
                elif direction == "right":
                    xi = int(container_rect.x + container_rect.width * (1 - deadzone))
                    xf = int(container_rect.x + container_rect.width * deadzone)
                else:
                    raise NotImplementedError
                TouchAction(cast(WebDriver, self.page.driver)).press(x=xi, y=yi).wait(1000).move_to(
                    x=xf, y=yf
                ).release().perform()
        logger.error(f"Cannot locate Element <{self}> after {tries} times of scrolling.")
        raise ElementNotFoundException(self)
