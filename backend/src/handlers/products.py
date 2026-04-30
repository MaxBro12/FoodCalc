from fastapi import HTTPException, status
from src.database import DataBase


class ProductsHandler:
    """
    Обработчик запросов к таблице продуктов.
    Связывает fastapi запросы с sqlalchemy.
    Используется только если данные нужно конвертировать.
    """

    def __init__(self, db: DataBase):
        self.db = db

    async def all(self, skip: int | None = 0, limit: int | None = 100) -> dict:
        """
        Возвращает список всех продуктов.
        """
        products = await self.db.products.pagination(
            skip=skip or 0,
            limit=limit or 100,
            load_relations=True
        )
        return {'products': [product.__dict__ for product in products]}

    async def by_id(self, product_id: int):
        """
        Возвращает продукт по его идентификатору.
        """
        product = await self.db.products.by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Данный минерал не найден'
            )
        return product

    async def search(self, query: str) -> dict:
        """
        Возвращает список названий продуктов, соответствующих поисковому запросу.
        """
        return {'names': [{
            'id': i[0],
            'name': i[1],
            'search_index': i[2]
        } for i in await self.db.products.search(query=query)]}

    async def names(self, limit: int = 500) -> dict:
        """
        Возвращает список названий продуктов. Необходимо для поиска.
        """
        return {'names': [{
            'id': i[0],
            'name': i[1],
            'search_index': i[2]
        } for i in await self.db.products.names(limit=limit)]}

    async def new(
        self,
        product: dict,
        user_id: int,
    ) -> dict:
        """
        Добавляет новый продукт в базу данных.
        """
        try:
            return {'ok': await self.db.products.new(
                pid=product['id'],
                name=product['name'],
                description=product['description'],
                calories_per_100g=product['calories_per_100g'],
                proteins_per_100g=product['proteins_per_100g'],
                fats_per_100g=product['fats_per_100g'],
                carbs_per_100g=product['carbs_per_100g'],
                fiber_per_100g=product['fiber_per_100g'],
                sugar_per_100g=product['sugar_per_100g'],
                added_by_id=user_id,
            )}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Неверные данные'
            )
