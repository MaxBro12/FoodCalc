from sqlalchemy.ext.asyncio import AsyncSession

from .base import Repository
from app.database.models import MineralType


class MineralTypeRepo(Repository):
    def __init__(self):
        super().__init__(MineralType, tuple('minerals'))

    async def exists_by_id(self, mineral_type_id: int, session: AsyncSession) -> bool:
        return await self._exists(f"{self.table_name}.id={mineral_type_id}", session=session)

    async def new(self, name: str, description: str, session: AsyncSession, commit: bool = True) -> bool:
        return await self.add(MineralType(name=name, description=description), session=session, commit=commit)

    async def by_id(self, type_id: int, session: AsyncSession, load_relation: bool = False) -> MineralType | None:
        return await self.get(f'{self.table_name}.id={type_id}', session=session, load_relations=load_relation)

    async def by_name(self, name: str, session: AsyncSession, load_relation: bool = False) -> MineralType | None:
        return await self.get(f"{self.table_name}.name='{name}'", session=session, load_relations=load_relation)
