from sqlalchemy.ext.asyncio import AsyncSession

from core.sql_repository import Repository
from app.database.models import MineralType


class MineralTypeRepo(Repository):
    def __init__(self, session: AsyncSession):
        super().__init__(MineralType, session=session, relationships=('minerals',))

    async def exists_by_id(self, mineral_type_id: int) -> bool:
        return await self._exists(f"{self.table_name}.id={mineral_type_id}")

    async def exists_by_name(self, mineral_type_name: str) -> bool:
        return await self._exists(f"{self.table_name}.name='{mineral_type_name}'")

    async def new(
        self,
        name: str,
        description: str,
        commit: bool = True
    ) -> bool:
        return await self.add(
            MineralType(name=name, description=description),
            commit=commit
        )

    async def by_id(
        self,
        type_id: int,
        load_relations: bool = False
    ) -> MineralType | None:
        return await self.get(
            f'{self.table_name}.id={type_id}',
            load_relations=load_relations
        )

    async def by_name(
        self,
        name: str,
        load_relation: bool = False
    ) -> MineralType | None:
        return await self.get(
            f"{self.table_name}.name='{name}'",
            load_relations=load_relation
        )

    async def del_by_id(self, type_id: int) -> bool:
        obj = await self.by_id(type_id=type_id)
        if obj is not None:
            return await self.delete(obj=obj, commit=True)
        return False

    async def pagination(self, skip: int, limit: int = 10, load_relations: bool = False) -> list[MineralType]:
        return await self._pagination(
            skip=skip,
            limit=limit,
            order_by_field='id',
            load_relations=load_relations
        )

    async def pagination(self, skip: int = 0, limit: int = 10, load_relations: bool = False):
        return await self._pagination(
            skip=skip,
            limit=limit,
            order_by_field='id',
            load_relations=load_relations
        )
