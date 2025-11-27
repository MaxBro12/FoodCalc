from sqlalchemy.ext.asyncio import AsyncSession

from .base import Repository
from app.database.models import Key


class KeyRepo(Repository):
    def __init__(self):
        super().__init__(Key)

    async def exists(self, _hash: str, session: AsyncSession) -> bool:
        return await self._exists(f"{self.table_name}.hash='{_hash}'", session=session)

    async def by_hash(
        self,
        key_hash: str,
        session: AsyncSession,
        load_relations: bool = False
    ) -> Key | None:
        return await self.get(
            f"{self.table_name}.hash='{key_hash}'",
            session=session,
            load_relations=load_relations
        )
