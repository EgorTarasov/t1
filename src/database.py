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
