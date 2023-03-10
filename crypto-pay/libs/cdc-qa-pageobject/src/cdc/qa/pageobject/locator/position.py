from __future__ import annotations

from .locator import Locator


class PositionLocator(Locator):
    """A `Locator` used in locating element with position."""

    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
