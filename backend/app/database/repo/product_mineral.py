
from sqlalchemy.ext.asyncio import AsyncSession

from .base import Repository
from app.database.models import ProductMineral


class ProductMineralRepo(Repository):
    def __init__(self):
        super().__init__(ProductMineral, ('product', 'mineral'))

    async def exists_by_id(self, product_id: int, mineral_id: int, session: AsyncSession) -> bool:
        return await self._exists(
            f"{self.table_name}.product_id={product_id} AND {self.table_name}.mineral_id={mineral_id}",
            session=session
        )

    async def new(
        self,
        product_id: int,
        mineral_id: int,
        content: float,
        session: AsyncSession,
        commit: bool = False
    ) -> bool:
        return await self.add(
            ProductMineral(product_id=product_id, mineral_id=mineral_id, content=content),
            session=session,
            commit=commit
        )
