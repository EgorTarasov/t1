from loguru import logger
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.auth.router import router as auth_router
from src.config import Config, app_config
from src.database import Database
from src.dependencies import DatabaseMiddleware
from src.email.config import EmailConfig, email_config
from src.email.dependencies import EmailClientMiddleware
from src.email.service import EmailClient
from src.hr.router import router as vacancy_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("connecting to db")

    db = Database(str(app_config.get().postgres_dsn))
    if not await db.check_connection():
        raise ValueError("Database is not available")
    else:
        logger.info("connected to db")
    email_client = EmailClient(**dict(email_config.get()))
    DatabaseMiddleware.set_db(db)
    EmailClientMiddleware.set_email_client(email_client)
    logger.info("starting app")
    yield None


def create_app() -> FastAPI:

    email_config.set(EmailConfig())  # type: ignore
    app_config.set(Config())  # type: ignore

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
    app.include_router(vacancy_router)
    return app


if __name__ == "__main__":
    try:
        import uvicorn

        uvicorn.run(
            create_app(),
            host="0.0.0.0",
        )
        app: FastAPI = create_app()
    except ImportError:
        print("uvicorn is not installed")
