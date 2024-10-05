from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from loguru import logger

from src.database import db
from src.hr.router import router as vacancy_router

from .auth.router import router as auth_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Lifespan of fastapi application with some runtime checks before running application"""
    logger.info("connecting to db")

    if not await db.check_connection():
        raise ValueError("Database is not available")
    else:
        logger.info("connected to db")

    logger.info("starting app")
    yield None


def create_app() -> FastAPI:
    """factory for creating api client with fastapi"""

    _app = FastAPI(
        title="Динозаврики мисис",
        version="0.0.1",
        description="Rest api for frontend Application",
        lifespan=lifespan,
    )

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_credentials=True,
        allow_headers=["*"],
    )
    add_pagination(_app)
    _app.include_router(auth_router)
    _app.include_router(vacancy_router)
    return _app


app: FastAPI = create_app()
