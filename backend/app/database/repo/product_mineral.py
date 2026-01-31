
from sqlalchemy.ext.asyncio import AsyncSession

from core.sql_repository import Repository
from app.database.models import ProductMineral


class ProductMineralRepo(Repository):
    def __init__(self, session: AsyncSession):
        super().__init__(ProductMineral, session=session, relationships=('product', 'mineral'))

    async def exists_by_id(self, product_id: int, mineral_id: int) -> bool:
        return await self._exists(
            f"{self.table_name}.product_id='{product_id}' AND {self.table_name}.mineral_id={mineral_id}"
        )

    async def new(
        self,
        product_id: str,
        mineral_id: int,
        content: float,
        commit: bool = False
    ) -> bool:
        return await self.add(
            ProductMineral(product_id=product_id, mineral_id=mineral_id, content=content),
            commit=commit
        )
