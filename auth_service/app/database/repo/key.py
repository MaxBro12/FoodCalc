from sqlalchemy.ext.asyncio import AsyncSession

from .base import Repository
from app.database.models import Key


class KeyRepo(Repository):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Key, session=session)

    async def exists(self, _hash: str) -> bool:
        return await self._exists(f"{self.table_name}.hash='{_hash}'")

    async def by_hash(
        self,
        key_hash: str,
        load_relations: bool = False
    ) -> Key | None:
        return await self.get(
            f"{self.table_name}.hash='{key_hash}'",
            load_relations=load_relations
        )
