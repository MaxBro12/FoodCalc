from sqlalchemy import select, exists

from app.database.models import Key
from app.database.database import Base, engine, new_session

from app.settings import settings


async def init_db():
    async with engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    if settings.DEBUG:
        async with new_session() as session:
            if not await session.scalar(select(exists().select_from(Key).where(Key.id == 1))):
                session.add(Key(id=1, value="123"))
                await session.commit()
