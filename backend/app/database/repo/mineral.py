from sqlalchemy.ext.asyncio import AsyncSession

from core.sql_repository import Repository
from app.database.models import Mineral


class MineralRepo(Repository):
    def __init__(self, session: AsyncSession):
        super().__init__(Mineral, session=session, relationships=('type', 'products'))

    async def exists_by_id(self, mineral_id: int) -> bool:
        return await self._exists(f"{self.table_name}.id={mineral_id}")

    async def exists_by_name(self, name: str) -> bool:
        return await self._exists(f"{self.table_name}.name='{name}'")

    async def new(
        self,
        name: str,
        compact_name: str,
        description: str,
        intake: float,
        type_id: int,
        commit: bool = True
    ) -> bool:
        return await self.add(
            Mineral(name=name, compact_name=compact_name, description=description, intake=intake, type_id=type_id),
            commit=commit
        )

    async def by_id(
        self, type_id: int,
        load_relations: bool = False
    ) -> Mineral | None:
        return await self.get(
            f'{self.table_name}.id={type_id}',
            load_relations=load_relations
        )

    async def by_name(
        self, name: str, load_relation: bool = False
    ) -> Mineral | None:
        return await self.get(
            f"{self.table_name}.name='{name}'",
            load_relations=load_relation
        )

    async def del_by_id(self, mineral_id: int) -> bool:
        obj = await self.by_id(type_id=mineral_id)
        if obj is not None:
            return await self.delete(obj=obj, commit=True)
        return False

    async def pagination(self, skip: int = 0, limit: int = 10, load_relations: bool = False):
        return await self._pagination(
            skip=skip,
            limit=limit,
            order_by_field='id',
            load_relations=load_relations
        )
