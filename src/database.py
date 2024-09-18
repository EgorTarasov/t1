from contextvars import ContextVar
import typing as tp
from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
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

    async def get_session(
        self,
    ) -> tp.AsyncGenerator[async_scoped_session[AsyncSession], tp.Any]:

        session: async_scoped_session[AsyncSession] = self.get_scoped_session()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
