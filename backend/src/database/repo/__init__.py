from sqlalchemy.ext.asyncio import AsyncSession

from core.sql_repository import DataBaseRepo

from .mineral_type import MineralTypeRepo
from .mineral import MineralRepo
from .product import ProductRepo
from .product_mineral import ProductMineralRepo


class DataBase(DataBaseRepo):
    """
    Класс DataBase предоставляет доступ к репозиториям для работы с базой данных.
    """
    mineral_types: MineralTypeRepo
    minerals: MineralRepo
    products: ProductRepo
    products_minerals: ProductMineralRepo

    def __init__(self, session: AsyncSession) -> None:
        self.mineral_types = MineralTypeRepo(session=session)
        self.minerals = MineralRepo(session=session)

        self.products = ProductRepo(session=session)
        self.products_minerals = ProductMineralRepo(session=session)

        super().__init__(session=session)
