import glob
import typing as tp

from src.database import Database

from sqlalchemy.ext.asyncio import AsyncSession


class DatabaseMiddleware:
    db: tp.Optional[Database] = None

    @staticmethod
    def set_db(database: Database):
        print(id(database), "db in set_db")
        DatabaseMiddleware.db = database

    @staticmethod
    async def get_session() -> tp.AsyncGenerator[AsyncSession, None]:
        print(id(DatabaseMiddleware.db), "db in get_session")
        if DatabaseMiddleware.db is None:
            raise ValueError("Database is not initialized")
        else:
            async with DatabaseMiddleware.db.session_factory() as session:
                yield session
