from .element import Element
from .button import ButtonElement
from .text import TextElement
from ..base.text_button import TextButtonElement as BaseTextButtonElement


class TextButtonElement(BaseTextButtonElement, ButtonElement, TextElement, Element):
    pass
