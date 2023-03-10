import logging

from .element import Element
from ....locator import SelectorLocator, PositionLocator

logger = logging.getLogger(__name__)


class TextElement(Element):
    @property
    def text(self) -> str:
        if isinstance(self.locator, SelectorLocator):
            return self._web_element.text

        elif isinstance(self.locator, PositionLocator):
            # TODO: handle getting text with PositionLocator; maybe use OCR? or find the closest WebElement and get its text # noqa: E501
            logger.error("text() cannot be used on Element with PositionLocator.")
            raise ValueError

        else:
            raise ValueError
