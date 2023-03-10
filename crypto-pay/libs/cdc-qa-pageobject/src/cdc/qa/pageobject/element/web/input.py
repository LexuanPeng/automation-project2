from __future__ import annotations
from typing import TypeVar, Union

import logging

from .button import ButtonElement
from .text import TextElement

from ...locator import SelectorLocator, PositionLocator

T = TypeVar("T", bound="InputElement")

logger = logging.getLogger(__name__)


class InputElement(ButtonElement, TextElement):
    def input(self: T, value: Union[str, int, float]) -> T:
        if isinstance(self.locator, SelectorLocator):
            self._web_element.send_keys(str(value))

        elif isinstance(self.locator, PositionLocator):
            logger.error("input() cannot be used on Element with PositionLocator.")
            raise ValueError

        else:
            raise ValueError

        return self

    def clear(self: T) -> T:
        if isinstance(self.locator, SelectorLocator):
            self._web_element.clear()

        elif isinstance(self.locator, PositionLocator):
            logger.error("clear() cannot be used on Element with PositionLocator.")
            raise ValueError

        else:
            raise ValueError

        return self

    @property
    def value(self) -> str:
        if isinstance(self.locator, SelectorLocator):
            return self._web_element.get_attribute("value")

        elif isinstance(self.locator, PositionLocator):
            logger.error("value() cannot be used on Element with PositionLocator.")
            raise ValueError

        else:
            raise ValueError
