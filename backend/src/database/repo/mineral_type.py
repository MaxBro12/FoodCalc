from sqlalchemy.ext.asyncio import AsyncSession

from core.sql_repository import RepositoryObj
from src.database.models import MineralType


class MineralTypeRepo(RepositoryObj):
    """
    Репозиторий для работы с типами минералов.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(MineralType, session=session, relationships=('minerals',))

    async def exists_by_id(self, mineral_type_id: int) -> bool:
        """
        Проверяет, существует ли тип минерала по его идентификатору.
        """
        return await self._exists(MineralType.id == mineral_type_id)

    async def exists_by_name(self, mineral_type_name: str) -> bool:
        """
        Проверяет, существует ли тип Минерала по его имени.
        """
        return await self._exists(MineralType.name == mineral_type_name)

    async def new(
        self,
        name: str,
        description: str,
        commit: bool = True
    ) -> bool:
        """
        Создает новый тип Минерала.
        """
        return await self.add(
            MineralType(name=name, description=description),
            commit=commit
        )

    async def by_id(
        self,
        type_id: int,
        load_relations: bool = False
    ) -> MineralType | None:
        """
        Возвращает тип Минерала по его идентификатору или None, если тип не найден.
        """
        return await self.get(
            MineralType.id == type_id,
            load_relations=load_relations
        )

    async def by_name(
        self,
        name: str,
        load_relation: bool = False
    ) -> MineralType | None:
        """
        Возвращает тип Минерала по его имени или None, если тип не найден.
        """
        return await self.get(
            MineralType.name == name,
            load_relations=load_relation
        )

    async def del_by_id(self, type_id: int) -> bool:
        """
        Удаляет тип Минерала по его идентификатору.
        """
        obj = await self.by_id(type_id=type_id)
        if obj is not None:
            return await self.delete(obj=obj, commit=True)
        return False

    async def pagination(
        self,
        skip: int = 0,
        limit: int = 10,
        load_relations: bool = False
    ) -> tuple[MineralType, ...]:
        """
        Возвращает пагинированный список типов Минералов.
        """
        return await self._pagination(
            skip=skip,
            limit=limit,
            order_by_field='id',
            load_relations=load_relations
        )
