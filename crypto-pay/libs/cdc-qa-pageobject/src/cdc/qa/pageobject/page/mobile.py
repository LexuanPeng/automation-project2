from __future__ import annotations
from typing import TYPE_CHECKING

from .page import Page

if TYPE_CHECKING:
    from cdc.qa.core import MobileApp, MobileDevice
    from appium.webdriver.webdriver import WebDriver


class MobilePage(Page):
    def __init__(self, app: MobileApp, device: MobileDevice, driver: WebDriver, *args, **kwargs):
        self.app: MobileApp
        self.device: MobileDevice
        self.driver: WebDriver
        super().__init__(app, device, driver, *args, **kwargs)
