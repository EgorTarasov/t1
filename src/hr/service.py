from httpx import Client


class SearchEngineClient:
    def __init__(self) -> None:
        self.client = Client()
