import typing as tp

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import db


async def get_db() -> tp.AsyncGenerator[AsyncSession, None]:
    """Dependency injection for sqlalchemy async session"""
    if db is None:
        raise ValueError("Database is not initialized")
    else:
        async with db.session_factory() as session:
            yield session
