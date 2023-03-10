from .element import Element
from .button import ButtonElement
from ..base.input import InputElement as BaseInputElement


class InputElement(BaseInputElement, ButtonElement, Element):
    pass
