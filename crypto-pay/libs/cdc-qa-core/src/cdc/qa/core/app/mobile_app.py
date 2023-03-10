import os

from .app import App
from ..enums import Platform


class MobileApp(App):
    def __init__(
        self,
        *args,
        platform: str,
        version_number: str,
        build_number: str,
        app_id: str,
        app_path: str,
        options: dict = {},
        **kwargs,
    ):
        self.platform: Platform = Platform(platform)
        self.version_number: str = version_number
        self.build_number: str = build_number

        self.app_id = app_id
        self.app_path = app_path

        self.options: dict = options

        # Resolve local app path
        if self.app_path.startswith("./"):
            self.app_path = self.app_path.replace("./", os.getcwd(), 1)
