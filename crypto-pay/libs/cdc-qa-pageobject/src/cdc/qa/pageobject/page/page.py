from __future__ import annotations

from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

from ..element import Element

if TYPE_CHECKING:
    from cdc.qa.core import App, Device
    from selenium.webdriver.remote.webdriver import WebDriver


class Page(ABC):
    """An abstract class representing a basic page object."""

    def __init__(
        self,
        app: App,
        device: Device,
        driver: WebDriver,
        env: str = None,
        test_data: dict = None,
        page_name: str = None,
        apis=None,
    ):
        self.app: App = app
        self.device: Device = device
        self.driver = driver
        self.test_data = test_data
        self.env = env
        self.page_name = page_name
        self.apis = apis
        self._bind_all_elements()

    def _bind_all_elements(self):
        for attr_name in dir(self):
            try:
                attr = getattr(self, attr_name)
                if isinstance(attr, Element):
                    attr.bind(self)
            except Exception:
                pass

    @abstractmethod
    def here(self) -> bool:
        """Abstract method for checking if currently on this page.

        Returns:
            bool: True if currently on this page.
        """
        pass

    @abstractmethod
    def go(self):
        """Abstract method for going to this page."""
        pass
