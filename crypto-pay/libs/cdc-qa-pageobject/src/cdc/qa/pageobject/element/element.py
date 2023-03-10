from __future__ import annotations
from typing import TYPE_CHECKING, TypeVar, Optional, Union

from abc import ABC
import os
import logging
import copy

from ..common.exception import ElementNotBoundException
from ..common.rect import Rect
from ..common.coordinate import Coordinate
from ..locator import SelectorLocator, PositionLocator

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

if TYPE_CHECKING:
    from ..locator import Locator
    from ..page import Page
    from selenium.webdriver.remote.webelement import WebElement

T = TypeVar("T", bound="Element")

logger = logging.getLogger(__name__)

DEFAULT_WAIT_TIMEOUT = int(os.environ.get("PAGEOBJECT_DEFAULT_WAIT_TIMEOUT", 60))


class Element(ABC):
    """An abstract class representing a basic element."""

    def __init__(self, locator: Locator, page: Page = None):
        self.locator: Locator = locator
        self._page: Optional[Page] = page

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} object on {self._page}: {self.locator}>"

    @property
    def page(self) -> Page:
        if not self._page:
            raise ElementNotBoundException(self)
        return self._page

    def bind(self: T, page: Page) -> T:
        self._page = page
        return self

    def replace(self: T, __old: str, __new: str) -> T:
        if isinstance(self.locator, SelectorLocator):
            new = copy.copy(self)
            new.locator = self.locator.replace(__old, __new)
            return new

        elif isinstance(self.locator, PositionLocator):
            logger.error("`replace()` cannot be used on `Element` with `PositionLocator`.")
            raise ValueError

        else:
            raise ValueError

    @property
    def _web_element(self) -> WebElement:
        if isinstance(self.locator, SelectorLocator):
            return self.page.driver.find_element(by=self.locator.by, value=self.locator.value)

        elif isinstance(self.locator, PositionLocator):
            logger.error("`_web_element` cannot be used on `Element` with `PositionLocator`.")
            raise ValueError

        else:
            raise ValueError

    @property
    def rect(self) -> Rect:
        if isinstance(self.locator, SelectorLocator):
            return Rect(**self._web_element.rect)

        elif isinstance(self.locator, PositionLocator):
            return Rect(
                x=self.locator.x,
                y=self.locator.y,
                width=self.locator.width,
                height=self.locator.height,
            )

        else:
            raise ValueError

    @property
    def center(self) -> Coordinate:
        x = self.rect.x + self.rect.width / 2
        y = self.rect.y + self.rect.height / 2
        return Coordinate(x, y)

    def wait(self: T, condition=None, timeout: Optional[int] = None, no_exception: bool = False) -> T:
        if not condition:
            condition = EC.presence_of_element_located

        if not timeout:
            timeout = DEFAULT_WAIT_TIMEOUT

        if isinstance(self.locator, SelectorLocator):
            try:
                logger.debug(f"Wait Element {self} with condition {condition} and timeout {timeout}s.")
                WebDriverWait(self.page.driver, timeout).until(
                    condition((self.locator.by, self.locator.value)), message=str(self)
                )
            except Exception as e:
                if not no_exception:
                    raise e

        elif isinstance(self.locator, PositionLocator):
            logger.warning("`wait()` on `Element` with `PositionLocator` have no effect.")

        else:
            raise ValueError

        return self

    def wait_clickable(self: T, timeout: Optional[int] = None, no_exception: bool = False) -> T:
        return self.wait(condition=EC.element_to_be_clickable, timeout=timeout, no_exception=no_exception)

    def get_attribute(self, attribute: str) -> Optional[Union[str, dict]]:
        if isinstance(self.locator, SelectorLocator):
            return self._web_element.get_attribute(attribute)
        elif isinstance(self.locator, PositionLocator):
            logger.error("`get_attribute()` cannot be used on `Element` with `PositionLocator`.")
            raise ValueError
        else:
            raise ValueError

    @property
    def is_visible(self) -> bool:
        if isinstance(self.locator, SelectorLocator):
            is_visible = False
            try:
                is_visible = self._web_element.is_displayed()
            except NoSuchElementException:
                pass
            except Exception as e:
                raise e
            logger.debug(f"Element {self} is {'' if is_visible else 'not '}visible.")
            return is_visible

        elif isinstance(self.locator, PositionLocator):
            logger.error("`is_visible` cannot be used on `Element` with `PositionLocator`.")
            raise ValueError

        else:
            raise ValueError

    @property
    def is_present(self) -> bool:
        if isinstance(self.locator, SelectorLocator):
            is_present = False
            try:
                self._web_element
                is_present = True
            except NoSuchElementException:
                pass
            except Exception as e:
                raise e
            logger.debug(f"Element {self} is {'' if is_present else 'not '}present.")
            return is_present

        elif isinstance(self.locator, PositionLocator):
            logger.error("`is_present` cannot be used on `Element` with `PositionLocator`.")
            raise ValueError

        else:
            raise ValueError

    @property
    def is_enabled(self) -> bool:
        if isinstance(self.locator, SelectorLocator):
            is_enabled = False
            try:
                is_enabled = self._web_element.is_enabled()
            except NoSuchElementException:
                pass
            except Exception as e:
                raise e
            logger.debug(f"Mobile Element {self} is {'' if is_enabled else 'not '}enabled.")
            return is_enabled

        elif isinstance(self.locator, PositionLocator):
            logger.error("`is_enabled` cannot be used on `Element` with `PositionLocator`.")
            raise ValueError

        else:
            raise ValueError
