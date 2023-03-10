from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..element import Element


class ElementNotBoundException(Exception):
    """Raised when the `Element` is not bound to a `Page`."""

    def __init__(self, element: Element):
        self.element = element
        self.message = f"Element <{element}> is not bound to a Page."
        super().__init__(self.message)

    def __str__(self):
        return self.message


class ElementNotFoundException(Exception):
    """Raised when the `Element` is not found."""

    def __init__(self, element: Element):
        self.element = element
        self.message = f"Element <{element}> is not found."
        super().__init__(self.message)

    def __str__(self):
        return self.message
