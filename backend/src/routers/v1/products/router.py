from fastapi import APIRouter, HTTPException, status, Body

from src.depends import DBDep, UserDep
from src.routers.v1.products.models import NewProduct
from src.handlers.products import ProductsHandler
from core.pydantic_misc_models import Ok, Detail
from core.fast_depends import PaginationParams
from core.fast_decorators import cache, rate_limiter
from core.redis_client import RedisDep
from .models import (
    SearchProduct,
    MultipleProductsResponse,
    ProductResponse,
    ProductsNames,
    UpdateProduct,
)


products_router_v1 = APIRouter(prefix='/v1/products', tags=['products'])


@products_router_v1.get('', response_model=MultipleProductsResponse)
@cache(key='products_pagination', expire=60*15)
@rate_limiter(max_requests=100, time_delta=60)
async def products_pagination(db: DBDep, pagination: PaginationParams, redis: RedisDep):
    """
    Получение пагинированного списка продуктов.
    Ветка кэшируется на 15 минут. Максимум 100 запросов в минуту.
    """
    return await ProductsHandler(db).all(
        skip=pagination.skip,
        limit=pagination.limit,
        redis=redis
    )


@products_router_v1.get('/details/{product_id}', response_model=ProductResponse, responses={
    200: {'model': ProductResponse, 'description': 'Успешно'},
    404: {'model': Detail, 'description': 'Продукт по заданному ID не найден'},
})
@cache(key='product_by_id', expire=60*60)
@rate_limiter(max_requests=100, time_delta=60)
async def product_by_id(product_id: str, db: DBDep, redis: RedisDep):
    """
    Получение информации о продукте по его ID.
    Ветка кэшируется на 1 час. Максимум 100 запросов в минуту.
    """
    return await ProductsHandler(db).by_id(product_id, redis=redis)


@products_router_v1.post('/search', response_model=ProductsNames)
@cache(key='search_products', expire=60*15)
@rate_limiter(max_requests=100, time_delta=60)
async def search_products(query: SearchProduct, db: DBDep, redis: RedisDep):
    """
    Поиск продуктов по имени или ID/barcode. Возвращает список найденных продуктов.
    Если данных не будет найдено, возвращает пустой список.
    Ветка кэшируется на 15 минут. Максимум 100 запросов в минуту.
    """
    return await ProductsHandler(db).search(query.id_or_name)


@products_router_v1.get('/names', response_model=ProductsNames)
@cache(key='product_names', expire=60*15)
@rate_limiter(max_requests=100, time_delta=60)
async def names(db: DBDep, redis: RedisDep, limit: int = 500):
    """
    Возвращает список имен продуктов необходимых для поисковых запросов.
    Ветка кэшируется на 15 минут. Максимум 100 запросов в минуту.
    """
    return await ProductsHandler(db).names(limit=limit)


@products_router_v1.post('/new', response_model=Ok, responses={
    200: {'model': Ok},
    400: {'model': Detail, 'description': 'Не удалось сохранить продукт'},
    409: {'model': Detail, 'description': 'Код продукта уже существует'}
})
async def save_new_product(new: NewProduct, db: DBDep, user: UserDep):
    if await db.products.exists_by_id(new.id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Продукт уже существует'
        )
    return await ProductsHandler(db).new(product=new.dict(), user_id=user.id)


@products_router_v1.delete('/{product_id}', response_model=Ok)
@rate_limiter(max_requests=10, time_delta=60)
async def del_product(product_id: str, db: DBDep, user: UserDep):
    """
    Удаляет продукт по его идентификатору.
    Доступно только для аутентифицированных пользователей.
    Разрешен только 10 запросов в минуту.
    """
    return {'ok': await db.products.del_by_id(product_id=product_id)}


@products_router_v1.put('/{product_id}', response_model=Ok, responses={
    200: {'model': Ok},
    400: {'model': Detail, 'description': 'Неверные данные'},
    401: {'model': Detail, 'description': 'Пользователь не аутентифицирован'},
    403: {'model': Detail, 'description': 'Недостаточно прав'},
    404: {'model': Detail, 'description': 'Продукт не найден'}
})
@rate_limiter(max_requests=10, time_delta=60)
async def update_product(
    product_id: str,
    new: UpdateProduct,
    db: DBDep,
    user: UserDep,
    redis: RedisDep
):
    """
    Обновляет статус  продукт по его идентификатору.
    """
    return await ProductsHandler(db).update(
        product_id=product_id,
        new=new.model_dump(),
        user=user,
        redis=redis
    )
