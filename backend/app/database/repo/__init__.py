from sqlalchemy.ext.asyncio import AsyncSession

from app.core.single import Singleton
from app.database.session import get_session
from .key import KeyRepo
from .user import UserRepo
from .mineral_type import MineralTypeRepo
from .mineral import MineralRepo
from .product import ProductRepo
from .product_mineral import ProductMineralRepo


class DataBase:
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session
        self.keys = KeyRepo(session=session)
        self.users = UserRepo(session=session)

        self.mineral_types = MineralTypeRepo(session=session)
        self.minerals = MineralRepo(session=session)

        self.products = ProductRepo(session=session)
        self.products_minerals = ProductMineralRepo(session=session)

    async def commit(self):
        await self.__session.commit()

    async def flush(self):
        await self.__session.flush()

    async def rollback(self):
        await self.__session.rollback()

    async def close(self):
        await self.__session.close()
