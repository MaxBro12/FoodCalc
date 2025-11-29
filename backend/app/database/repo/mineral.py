from sqlalchemy.ext.asyncio import AsyncSession

from .base import Repository
from app.database.models import Mineral


class MineralRepo(Repository):
    def __init__(self):
        super().__init__(Mineral, ('type', 'products'))

    async def exists_by_id(self, mineral_id: int, session: AsyncSession) -> bool:
        return await self._exists(f"{self.table_name}.id={mineral_id}", session=session)

    async def new(
        self,
        name: str,
        description: str,
        intake: float,
        type_id: int,
        session: AsyncSession,
        commit: bool = True
    ) -> bool:
        return await self.add(
            Mineral(name=name, description=description, intake=intake, type_id=type_id),
            session=session,
            commit=commit
        )

    async def by_id(self, type_id: int, session: AsyncSession, load_relation: bool = False) -> Mineral | None:
        return await self.get(f'{self.table_name}.id={type_id}', session=session, load_relations=load_relation)

    async def by_name(self, name: str, session: AsyncSession, load_relation: bool = False) -> Mineral | None:
        return await self.get(f"{self.table_name}.name='{name}'", session=session, load_relations=load_relation)

    async def del_by_id(self, mineral_id: int, session: AsyncSession) -> bool:
        obj = await self.by_id(type_id=mineral_id, session=session)
        if obj is not None:
            return await self.delete(obj=obj, session=session, commit=True)
        return False
