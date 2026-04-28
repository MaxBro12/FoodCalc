from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from core.sql_repository import RepositoryObj
from src.database.models import ProductMineral


class ProductMineralRepo(RepositoryObj):
    """
    Репозиторий для работы с связями между продуктами и минералами в базе данных.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(ProductMineral, session=session, relationships=('product', 'mineral'))

    async def exists_by_id(self, product_id: int, mineral_id: int) -> bool:
        """
        Проверяет, существует ли связь между продуктом и минералом по их идентификаторам.
        """
        return await self._exists(and_(
            ProductMineral.product_id == product_id,
            ProductMineral.mineral_id == mineral_id
        ))

    async def new(
        self,
        product_id: str,
        mineral_id: int,
        content: float,
        commit: bool = False
    ) -> bool:
        """
        Создает новую связь между продуктом и минералом в базе данных.
        """
        return await self.add(
            ProductMineral(
                product_id=product_id,
                mineral_id=mineral_id,
                content=content
            ),
            commit=commit
        )
