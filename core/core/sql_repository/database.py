from sqlalchemy.ext.asyncio import AsyncSession


class DataBaseRepo:
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def commit(self):
        await self.__session.commit()

    async def flush(self):
        await self.__session.flush()

    async def rollback(self):
        await self.__session.rollback()

    async def close(self):
        await self.__session.close()
