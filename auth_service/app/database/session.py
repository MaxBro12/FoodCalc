from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from .database import new_session
from app.core.debug import logger


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with new_session() as session:
        try:
            session.begin()
            yield session
            await session.commit()
        except Exception as e:
            logger.log(e, 'crit')
            await session.rollback()
            raise e
