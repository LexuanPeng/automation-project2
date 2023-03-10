from __future__ import annotations
from typing import TypeVar

import copy

from .locator import Locator

T = TypeVar("T", bound="SelectorLocator")


class SelectorLocator(Locator):
    """A `Locator` used in locating element with selector."""

    def __init__(self, by: str, value: str):
        self.by: str = by
        self.value: str = value

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} object: ({self.by}, {self.value})>"

    def replace(self: T, __old: str, __new: str) -> T:
        new = copy.copy(self)
        new.value = self.value.replace(__old, __new)
        return new
