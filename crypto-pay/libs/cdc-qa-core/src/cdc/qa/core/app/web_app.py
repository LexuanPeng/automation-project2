from .app import App


class WebApp(App):
    def __init__(
        self,
        *args,
        base_url: str,
        paths: dict,
        options: dict = {},
        **kwargs,
    ):
        self.base_url: str = base_url
        self.paths: dict = paths

        self.options: dict = options
