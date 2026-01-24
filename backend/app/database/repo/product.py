from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from .base import Repository
from app.database.models import Product


class ProductRepo(Repository):
    def __init__(self, session: AsyncSession):
        super().__init__(Product, session=session, relationships=('type', 'minerals'))

    async def exists_by_id(self, mineral_id: int) -> bool:
        return await self._exists(f"{self.table_name}.id={mineral_id}")

    async def new(
        self,
        pid: str,
        name: str,
        description: str,
        calories: int,
        energy: int,
        added_by_id: int,
        commit: bool = False
    ) -> bool:
        return await self.add(
            Product(
                id=pid,
                name=name,
                description=description,
                calories=calories,
                energy=energy,
                added_by_id=int(added_by_id)
            ),
            commit=commit
        )

    async def by_id(
        self,
        type_id: str,
        load_relations: bool = False
    ) -> Product | None:
        return await self.get(
            f"{self.table_name}.id='{type_id}'",
            load_relations=load_relations
        )

    async def by_name(
        self,
        name: str,
        load_relations: bool = False
    ) -> Product | None:
        return await self.get(
            f"{self.table_name}.name='{name}'",
            load_relations=load_relations
        )

    async def del_by_id(self, product_id: str) -> bool:
        obj = await self.by_id(type_id=product_id)
        if obj is not None:
            return await self.delete(obj=obj, commit=True)
        return False

    async def names(self, limit: int = 500) -> list[tuple[str, str, float]]:
        return (await self.session.execute(select(
            Product.id,
            Product.name,
            Product.search_index
        ).limit(limit))).all()

    async def search(self, query: str, limit: int = 500) -> list[tuple[str, str, float]]:
        ans = (await self.session.execute(
            select(
                Product.id,
                Product.name,
                Product.search_index
            ).where(func.lower(Product.name).like(f'%{query.lower()}%')).limit(limit)
        )).all()
        if len(ans) == 0:
            return (await self.session.execute(select(
                Product.id,
                Product.name,
                Product.search_index
            ).where(Product.id.like(f'%{query}%')).limit(limit))).all()
        return ans
