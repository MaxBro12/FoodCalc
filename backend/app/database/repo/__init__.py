from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from core.sql_repository import DataBaseRepo
from .mineral_type import MineralTypeRepo
from .mineral import MineralRepo
from .product import ProductRepo
from .product_mineral import ProductMineralRepo


class DataBase(DataBaseRepo):
    def __init__(self, session: AsyncSession) -> None:
        self.mineral_types = MineralTypeRepo(session=session)
        self.minerals = MineralRepo(session=session)

        self.products = ProductRepo(session=session)
        self.products_minerals = ProductMineralRepo(session=session)

        super().__init__(session=session)
