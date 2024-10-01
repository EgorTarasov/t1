from .service import SearchEngineClient
import typing as tp


class SearchEngineClientMiddleware:
    search_engine_client: SearchEngineClient | None = None

    @staticmethod
    def set_search_engine_client(search_engine_client: SearchEngineClient):
        SearchEngineClientMiddleware.search_engine_client = search_engine_client

    @staticmethod
    async def get_client() -> tp.AsyncGenerator[SearchEngineClient, None]:
        if SearchEngineClientMiddleware.search_engine_client is None:
            raise ValueError("Search engine client is not initialized")
        else:
            yield SearchEngineClientMiddleware.search_engine_client
