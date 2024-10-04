import glob
import typing as tp

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Database


class DatabaseMiddleware:
    db: tp.Optional[Database] = None

    @staticmethod
    def set_db(database: Database):
        DatabaseMiddleware.db = database

    @staticmethod
    async def get_session() -> tp.AsyncGenerator[AsyncSession, None]:
        if DatabaseMiddleware.db is None:
            raise ValueError("Database is not initialized")
        else:
            async with DatabaseMiddleware.db.session_factory() as session:
                yield session
