import logging

from .element import Element
from .button import ButtonElement
from ..base.text_button import TextButtonElement as BaseTextButtonElement
from ....locator import SelectorLocator, PositionLocator

logger = logging.getLogger(__name__)


class TextButtonElement(BaseTextButtonElement, ButtonElement, Element):
    @property
    def label(self) -> str:
        if isinstance(self.locator, SelectorLocator):
            return self._web_element.get_attribute("label")

        elif isinstance(self.locator, PositionLocator):
            # TODO: handle getting text with PositionLocator; maybe use OCR? or find the closest WebElement and get its text # noqa: E501
            logger.error("text() cannot be used on Element with PositionLocator.")
            raise ValueError

        else:
            raise ValueError

    @property
    def name(self) -> str:
        if isinstance(self.locator, SelectorLocator):
            return str(self._web_element.get_attribute("name"))

        elif isinstance(self.locator, PositionLocator):
            # TODO: handle getting text with PositionLocator; maybe use OCR? or find the closest WebElement and get its text # noqa: E501
            logger.error("text() cannot be used on Element with PositionLocator.")
            raise ValueError

        else:
            raise ValueError
