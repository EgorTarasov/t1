import logging
from contextlib import asynccontextmanager
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from src.config import app_config, Config
from src.database import Database
from src.dependencies import DatabaseMiddleware
from src.auth.router import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    db = Database(app_config.get().postgres_dsn)
    DatabaseMiddleware.set_db(db)
    print("db in lifespan", db)
    yield None
    # TODO: close db connection


def create_app() -> FastAPI:
    app_config.set(Config())  # type: ignore
    logging.basicConfig(
        level=app_config.get().logging_level,
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
    app.include_router(auth_router)

    return app


app: FastAPI = create_app()
