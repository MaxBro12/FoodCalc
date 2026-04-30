from sqlalchemy.ext.asyncio import AsyncSession

from core.sql_repository import RepositoryObj
from src.database.models import Mineral


class MineralRepo(RepositoryObj):
    """
    Репозиторий для работы с моделью Mineral.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(Mineral, session=session, relationships=('type', 'products'))

    async def exists_by_id(self, mineral_id: int) -> bool:
        """
        Проверяет, существует ли минерал по его идентификатору.
        """
        return await self._exists(Mineral.id == mineral_id)

    async def exists_by_name(self, name: str) -> bool:
        """
        Проверяет, существует ли минерал по его имени.
        """
        return await self._exists(Mineral.name == name)

    async def new(
        self,
        name: str,
        compact_name: str,
        description: str,
        daily_value: float,
        type_id: int,
        commit: bool = True
    ) -> bool:
        """
        Создает новый минерал.
            - name: имя минерала
            - compact_name: компактное имя минерала
            - description: описание минерала
            - daily_value: среднее потребление минерала в миллиграммах в день
            - type_id: идентификатор типа минерала
            - commit: если True, то коммитит изменения в базу данных
        """
        return await self.add(
            Mineral(
                name=name,
                compact_name=compact_name,
                description=description,
                daily_value=daily_value,
                type_id=type_id
            ),
            commit=commit
        )

    async def by_id(
        self,
        mineral_id: int,
        load_relations: bool = False
    ) -> Mineral | None:
        """
        Метод возвращает минерал по его идентификатору или None, если минерал не найден
        """
        return await self.get(
            Mineral.id == mineral_id,
            load_relations=load_relations
        )

    async def by_name(
        self, name: str, load_relation: bool = False
    ) -> Mineral | None:
        """
        Метод возвращает минерал по его имени или None, если минерал не найден
        """
        return await self.get(
            Mineral.name == name,
            load_relations=load_relation
        )

    async def del_by_id(self, mineral_id: int) -> bool:
        """
        Метод удаляет минерал по его идентификатору
        """
        obj = await self.by_id(mineral_id=mineral_id)
        if obj is not None:
            return await self.delete(obj=obj, commit=True)
        return False

    async def pagination(
        self,
        skip: int = 0,
        limit: int = 10,
        load_relations: bool = False
    ) -> tuple[Mineral, ...]:
        """
        Метод возвращает пагинированный кортеж минералов
        """
        return await self._pagination(
            skip=skip,
            limit=limit,
            order_by_field='id',
            load_relations=load_relations
        )
