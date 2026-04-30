from fastapi import APIRouter, HTTPException, status

from src.depends import UserDep, DBDep
from src.handlers import MineralsHandler, MineralTypesHandler
from core.pydantic_misc_models import Ok, Detail
from core.fast_depends import PaginationParams
from core.fast_decorators import cache, rate_limiter
from core.redis_client import RedisDep
from .models import (
    MineralResponse,
    MultipleMineralResponse,
    MineralTypeResponse,
    MultipleMineralTypeResponse,
)


minerals_router_v1 = APIRouter(prefix='/v1/universe', tags=['minerals and types'])


@minerals_router_v1.get('/minerals', response_model=MultipleMineralResponse)
@cache(key='minerals_pagination', expire=60*60)
@rate_limiter(max_requests=100, time_delta=60)
async def minerals_pagination(db: DBDep, pagination: PaginationParams, redis: RedisDep):
    """
    Получение пагинированного списка минералов.
    Ветка кэшируется на 1 час. 100 запросов в минуту.
    """
    return await MineralsHandler(db).all(skip=pagination.skip, limit=pagination.limit)


@minerals_router_v1.get('/minerals/{mineral_id}', response_model=MineralResponse, responses={
    200: {'model': MineralResponse},
    404: {'model': Detail, 'description': 'Mineral not found'}
})
@cache(key='mineral_by_id', expire=60*60)
@rate_limiter(max_requests=100, time_delta=60)
async def mineral_by_id(mineral_id: int, db: DBDep, redis: RedisDep):
    """
    Получение минерала по его ID.
    Ветка кэшируется на 1 час. 100 запросов в минуту.
    """
    return await MineralsHandler(db).by_id(mineral_id)


@minerals_router_v1.get('/types', response_model=MultipleMineralTypeResponse)
@cache(key='mineral_types_pagination')
async def mineral_types_pagination(db: DBDep, pagination: PaginationParams, redis: RedisDep):
    return await MineralTypesHandler(db).all(skip=pagination.skip, limit=pagination.limit)


@minerals_router_v1.get('/types/{type_id}', response_model=MineralTypeResponse)
@cache(key='mineral_type_by_id')
async def type_by_id(type_id: int, db: DBDep, redis: RedisDep):
    return await MineralTypesHandler(db).by_id(type_id)
