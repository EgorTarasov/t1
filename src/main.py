import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import config, Config
from database import Database, db


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.set(Database(config.get().postgres_dsn))
    yield None


def create_app() -> FastAPI:
    config.set(Config())  # type: ignore
    logging.basicConfig(
        level=config.get().logging_level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        filemode="w",
    )

    app = FastAPI(
        title="Динозаврики мисис",
        version="0.0.1",
        description="Rest api for frontend Application",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_credentials=True,
        allow_headers=["*"],
    )

    @app.get("/")
    async def health_check():
        return {"status": "ok"}

    # app.mount("/api/static", StaticFiles(directory="./backtests"), name="static")

    return app


app: FastAPI = create_app()
