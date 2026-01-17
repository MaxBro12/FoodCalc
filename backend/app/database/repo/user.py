from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User
from .base import Repository


class UserRepo(Repository):
    def __init__(self):
        super().__init__(User, ('key',))

    async def exists(self, username: str, session: AsyncSession) -> bool:
        return await self._exists(f"{self.table_name}.name='{username}'", session=session)

    async def by_name(
        self,
        username: str,
        session: AsyncSession,
        load_relations: bool = False
    ) -> User | None:
        return await super().get(
            f"{self.table_name}.name='{username}'",
            session=session,
            load_relations=load_relations
        )

    async def by_id(
        self,
        user_id: int,
        session: AsyncSession,
        load_relations: bool = False
    ) -> User | None:
        return await self.get(
            f"{self.table_name}.id={user_id}",
            session=session,
            load_relations=load_relations
        )

    async def new(
        self,
        username: str,
        password: str,
        is_admin: bool,
        key_id: int,
        session: AsyncSession,
        commit: bool = False
    ) -> bool:
        return await self.add(User(
            name=username,
            password=password,
            is_admin=is_admin,
            key_id=key_id,
        ), session=session, commit=commit)

    async def deactivate(
        self,
        user_id: int,
        session: AsyncSession,
    ) -> bool:
        user = await self.get(
            f"{self.table_name}.id={user_id}",
            session=session,
        )
        if user:
            user.is_active = False
            return True
        return False

    async def verify_tokens(
        self,
        user_id: int,
        unique: str,
        refresh_token: str,
        session: AsyncSession,
    ) -> bool:
        user = await self.get(
            f"{self.table_name}.id={user_id}",
            session=session,
        )
        if user:
            return True if user.unique == unique and user.refresh_token == refresh_token else False
        return False

    async def set_tokens(
        self,
        user_id: int,
        unique: str,
        refresh_token: str,
        session: AsyncSession,
    ) -> bool:
        user = await self.get(
            f"{self.table_name}.id={user_id}",
            session=session,
        )
        if user:
            user.unique = unique
            user.refresh_token = refresh_token
            return True
        return False

    async def clear_tokens(
        self,
        user_id: int,
        session: AsyncSession,
    ) -> bool:
        return await self.set_tokens(user_id, '', '', session)
