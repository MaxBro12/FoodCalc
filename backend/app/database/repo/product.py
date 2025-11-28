from sqlalchemy.ext.asyncio import AsyncSession

from .base import Repository
from app.database.models import Product


class ProductRepo(Repository):
    def __init__(self):
        super().__init__(Product, ('type', 'minerals'))

    async def exists_by_id(self, mineral_id: int, session: AsyncSession) -> bool:
        return await self._exists(f"{self.table_name}.id={mineral_id}", session=session)

    async def new(
        self,
        name: str,
        description: str,
        added_by_id: int,
        session: AsyncSession,
        commit: bool = True
    ) -> bool:
        return await self.add(
            Product(name=name, description=description, added_by_id=added_by_id),
            session=session,
            commit=commit
        )

    async def by_id(self, type_id: int, session: AsyncSession, load_relation: bool = False) -> Product | None:
        return await self.get(f'{self.table_name}.id={type_id}', session=session, load_relations=load_relation)

    async def by_name(self, name: str, session: AsyncSession, load_relation: bool = False) -> Product | None:
        return await self.get(f"{self.table_name}.name='{name}'", session=session, load_relations=load_relation)
