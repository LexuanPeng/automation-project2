from __future__ import annotations
from typing import TYPE_CHECKING
import logging

from .page import Page

if TYPE_CHECKING:
    from cdc.qa.core import WebApp, WebDevice
    from selenium.webdriver.remote.webdriver import WebDriver

logger = logging.getLogger(__name__)


class WebPage(Page):
    def __init__(self, app: WebApp, device: WebDevice, driver: WebDriver, *args, **kwargs):
        self.app: WebApp
        self.device: WebDevice
        super().__init__(app, device, driver, *args, **kwargs)

        self.base_url: str = self.app.base_url
        self.path: str = self.app.paths.get(self.__class__.__name__, None)

    @property
    def url(self):
        if not self.path:
            logger.warning(f"'path' is not set for Page '{self.__class__.__name__}'; is this correct?")
        return self.base_url + (self.path or "")

    def here(self) -> bool:
        """Check if currently on this page."""
        # TODO: implement checking url with parameters
        return self.driver.current_url == self.url

    def go(self):
        """Go to this page."""
        self.driver.get(self.url)
