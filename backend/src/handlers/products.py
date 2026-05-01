from core.redis_client import RedisClient
from fastapi import HTTPException, status
from src.database import DataBase, Product
from src.services.authservice import auth_service, User as UserFull
from src.handlers.auth import User


class ProductsHandler:
    """
    Обработчик запросов к таблице продуктов.
    Связывает fastapi запросы с sqlalchemy.
    Используется только если данные нужно конвертировать.
    """

    def __init__(self, db: DataBase):
        self.db = db

    @staticmethod
    async def _get_username(product: Product, redis: RedisClient) -> str:
        return (await auth_service.user_by_id(product.added_by, redis)).name

    @staticmethod
    def _product_to_dict(product: Product, username: str) -> dict:
        """
        Конвертирует модель Product в словарь.
        """
        return {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'calories_per_100g': product.calories_per_100g,
            'proteins_per_100g': product.proteins_per_100g,
            'fats_per_100g': product.fats_per_100g,
            'carbs_per_100g': product.carbs_per_100g,
            'fiber_per_100g': product.fiber_per_100g,
            'sugar_per_100g': product.sugar_per_100g,
            'likes': product.likes,
            'search_index': product.search_index,
            'created_at': product.created_at,
            'updated_at': product.updated_at,
            'added_by': username,
        }

    async def all(self, redis: RedisClient, skip: int | None = 0, limit: int | None = 100) -> dict:
        """
        Возвращает список всех продуктов.
        """
        products = await self.db.products.pagination(
            skip=skip or 0,
            limit=limit or 100,
            verified=True,
            load_relations=True
        )
        return {'products': [self._product_to_dict(
            product,
            await self._get_username(product, redis)
        ) for product in products]}

    async def by_id(self, product_id: str, redis: RedisClient):
        """
        Возвращает продукт по его идентификатору.
        """
        product = await self.db.products.by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Данный минерал не найден'
            )
        return self._product_to_dict(
            product,
            await self._get_username(product, redis)
        )

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
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Неверные данные'
            )

    async def update(
        self,
        product_id: str,
        new: dict,
        user: User,
        redis: RedisClient,
    ) -> dict:
        """
        Обновляет продукт в базе данных.
        """
        user_full = await auth_service.user_by_id(user.id, redis=redis)
        try:
            # Получаем продукт по идентификатору
            product = await self.db.products.by_id(product_id)
            if product is None:
                # Если продукт не найден, выбрасываем исключение
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Продукт не найден'
                )
            # Обновлять данные продукта могут только его добавивший или администратор
            if user.id != product.added_by or not user_full.is_admin:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail='Недостаточно прав'
                )

            if new.get('name'):
                product.name = new['name']
            if new.get('description'):
                product.description = new['description']
            if new.get('calories_per_100g'):
                product.calories_per_100g = new['calories_per_100g']
            if new.get('proteins_per_100g'):
                product.proteins_per_100g = new['proteins_per_100g']
            if new.get('fats_per_100g'):
                product.fats_per_100g = new['fats_per_100g']
            if new.get('carbs_per_100g'):
                product.carbs_per_100g = new['carbs_per_100g']
            if new.get('fiber_per_100g'):
                product.fiber_per_100g = new['fiber_per_100g']
            if new.get('sugar_per_100g'):
                product.sugar_per_100g = new['sugar_per_100g']
            if new.get('is_verified'):
                # Проводить верификацию могут только администраторы
                if user_full.is_admin:
                    product.is_verified = new['is_verified']
                else:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail='Недостаточно прав'
                    )
            return {'ok': True}
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Неверные данные'
            )
