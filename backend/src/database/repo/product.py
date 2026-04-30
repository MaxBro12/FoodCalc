from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from core.sql_repository import RepositoryObj
from src.database.models import Product


class ProductRepo(RepositoryObj):
    """
    Репозиторий для работы с продуктами в базе данных.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(Product, session=session, relationships=('type', 'minerals'))

    async def exists_by_id(self, product_id: str) -> bool:
        """
        Проверяет, существует ли продукт с указанным идентификатором.
        """
        return await self._exists(Product.id == product_id)

    async def new(
        self,
        pid: str,
        name: str,
        description: str,
        calories_per_100g: float,
        proteins_per_100g: float,
        fats_per_100g: float,
        carbs_per_100g: float,
        fiber_per_100g: float,
        sugar_per_100g: float,
        added_by_id: int,
        commit: bool = False
    ) -> bool:
        """
        Создает новый продукт и добавляет его в базу данных.
        """
        return await self.add(
            Product(
                id=pid,
                name=name,
                description=description,
                calories_per_100g=calories_per_100g,
                proteins_per_100g=proteins_per_100g,
                fats_per_100g=fats_per_100g,
                carbs_per_100g=carbs_per_100g,
                fiber_per_100g=fiber_per_100g,
                sugar_per_100g=sugar_per_100g,
                added_by=int(added_by_id)
            ),
            commit=commit
        )

    async def by_id(
        self,
        type_id: str,
        load_relations: bool = False
    ) -> Product | None:
        """
        Возвращает продукт по его идентификатору или None, если продукт не найден.
        """
        return await self.get(
            Product.id == type_id,
            load_relations=load_relations
        )

    async def by_name(
        self,
        name: str,
        load_relations: bool = False
    ) -> Product | None:
        """
        Возвращает продукт по его названию или None, если продукт не найден.
        """
        return await self.get(
            Product.name == name,
            load_relations=load_relations
        )

    async def not_verified(self) -> tuple[Product, ...]:
        """
        Возвращает продукты, которые не верифицированы администратором.
        """
        return await self.some(
            Product.is_verified == False
        )

    async def del_by_id(self, product_id: str) -> bool:
        """
        Удаляет продукт по его идентификатору.
        """
        obj = await self.by_id(type_id=product_id)
        if obj is not None:
            return await self.delete(obj=obj, commit=True)
        return False

    async def names(self, limit: int = 500) -> tuple[tuple[str, str, float], ...]:
        """
        Возвращает список названий продуктов с их идентификаторами и индексами поиска.
        """
        return tuple((await self.session.execute(select(
            Product.id,
            Product.name,
            Product.search_index
        ).limit(limit))).all())

    async def search(self, query: str, limit: int = 500) -> tuple[tuple[str, str, float], ...]:
        """
        Возвращает список продуктов, соответствующих поисковому запросу, с их идентификаторами и индексами поиска.
        """
        ans = (await self.session.execute(
            select(
                Product.id,
                Product.name,
                Product.search_index
            ).where(func.lower(Product.name).like(f'%{query.lower()}%')).limit(limit)
        )).all()
        if len(ans) == 0:
            return (await self.session.execute(select(
                Product.id,
                Product.name,
                Product.search_index
            ).where(Product.id.like(f'%{query}%')).limit(limit))).all()
        return tuple(ans)

    async def pagination(
        self, skip: int = 0, limit: int = 10,
        load_relations: bool = False
    ) -> tuple[Product, ...]:
        """
        Возвращает список продуктов с параметров пагинации.
        """
        return await self._pagination(
            skip=skip,
            limit=limit,
            order_by_field='id',
            load_relations=load_relations
        )
