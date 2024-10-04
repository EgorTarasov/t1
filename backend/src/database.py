import typing as tp
from asyncio import current_task

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, declared_attr

from src.config import app_config


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(self) -> str:
        name = self.__name__[0].lower() + self.__name__[1:]
        name = "".join(c if c.islower() else f"_{c.lower()}" for c in name)
        return f"{name}s"


class Database:
    def __init__(self, dsn: str, echo: bool = False) -> None:
        self.engine: AsyncEngine = create_async_engine(
            url=dsn,
            echo=echo,
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    def get_scoped_session(self) -> async_scoped_session[AsyncSession]:
        return async_scoped_session(self.session_factory, scopefunc=current_task)

    async def check_connection(self) -> bool:
        try:
            async with self.engine.connect() as conn:
                await conn.execute(sa.text("SELECT 1"))
            return True
        except Exception:
            return False

    async def get_session(
        self,
    ) -> tp.AsyncGenerator[async_scoped_session[AsyncSession], tp.Any]:

        if not await self.check_connection():
            raise ConnectionError("Database connection is not alive")

        session: async_scoped_session[AsyncSession] = self.get_scoped_session()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


db: Database = Database(str(app_config.postgres_dsn))
