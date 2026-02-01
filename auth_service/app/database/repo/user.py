from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User
from core.sql_repository import Repository
from core.security import SecurityService
from core.spec_time import get_current_time


class UserRepo(Repository):
    """Класс репозиторий для работы с пользователями"""
    def __init__(self, session: AsyncSession):
        super().__init__(User, session=session, relationships=('key',))

    async def exists(self, username: str) -> bool:
        return await self._exists(f"{self.table_name}.name='{username}'")

    async def by_name(
        self,
        username: str,
        load_relations: bool = False
    ) -> User | None:
        return await super().get(
            f"{self.table_name}.name='{username}'",
            load_relations=load_relations
        )

    async def by_id(
        self,
        user_id: int,
        load_relations: bool = False
    ) -> User | None:
        return await self.get(
            f"{self.table_name}.id={user_id}",
            load_relations=load_relations
        )

    async def new(
        self,
        username: str,
        password: str,
        is_admin: bool,
        key_id: int,
        commit: bool = False
    ) -> bool:
        return await self.add(User(
            name=username,
            password=password,
            is_admin=is_admin,
            key_id=key_id,
        ), commit=commit)

    async def deactivate(
        self,
        user_id: int,
    ) -> bool:
        user = await self.get(
            f"{self.table_name}.id={user_id}",
        )
        if user:
            user.is_active = False
            return True
        return False

    async def activate(
        self,
        user_id: int,
    ) -> bool:
        user = await self.get(
            f"{self.table_name}.id={user_id}",
        )
        if user:
            user.is_active = True
            return True
        return False

    async def check_password(
        self,
        user_name: str,
        password: str,
    ) -> User | None:
        """Проверка пароля пользователя, для этого пользователь должен быть активен"""
        user = await self.by_name(user_name)
        if user and user.is_active \
        and SecurityService.verify(password, user.password):
            user.last_active = get_current_time()
            return user

    async def verify_uni(
        self,
        user_id: int,
        uni: str,
    ) -> bool:
        """Проверка уникального идентификатора пользователя"""
        user = await self.get(
            f"{self.table_name}.id={user_id} AND {self.table_name}.unique='{uni}'",
        )
        if user:
            return True
        return False

    async def set_uni(
        self,
        user_id: int,
        uni: str,
    ) -> bool:
        """Установка уникального идентификатора пользователя"""
        user = await self.get(
            f"{self.table_name}.id={user_id}",
        )
        if user:
            user.unique = uni
            return True
        return False

    async def clear_uni(
        self,
        user_id: int,
    ) -> bool:
        """Очистка уникального идентификатора пользователя"""
        return await self.set_uni(user_id, '')
