from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from .database import new_session
from app.core.debug import logger


async def get_session() -> AsyncGenerator[AsyncSession]:
    try:
        async with new_session() as session:
            session.begin()
            yield session
            await session.commit()
    except Exception as e:
        logger.log(e, 'crit')
        await session.rollback()
        raise e
