import logging

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from .database import new_session


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with new_session() as session:
        try:
            session.begin()
            yield session
            await session.commit()
        except IntegrityError as e:
            await session.rollback()
