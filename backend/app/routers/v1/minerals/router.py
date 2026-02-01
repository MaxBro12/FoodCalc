from fastapi import APIRouter, HTTPException, status

from core.pydantic_misc_models import Ok
from core.fast_depends import PaginationParams
from core.fast_decorators import cache
from core.redis_client import RedisDep
from app.depends import UserDep, DBDep
from .models import (
    NewMineral,
    MineralResponse,
    MultipleMineralResponse,
    NewMineralType,
    MineralTypeResponse,
    MultipleMineralTypeResponse,
)


mineral_router_v1 = APIRouter(prefix='/v1/universe', tags=['minerals and types'])


@mineral_router_v1.get('/minerals/', response_model=MultipleMineralResponse)
@cache(key='minerals_pagination')
async def minerals_pagination(db: DBDep, pagination: PaginationParams, redis: RedisDep):
    minerals = await db.minerals.pagination(
        skip=pagination.skip,
        limit=pagination.limit,
        load_relations=True
    )
    return {'minerals': [{
        'id': mineral.id,
        'name': mineral.name,
        'compact_name': mineral.compact_name,
        'description': mineral.description,
        'intake': mineral.intake,
        'type_id': mineral.type_id,
        'type_name': mineral.type.name
    } for mineral in minerals]}


@mineral_router_v1.get('/minerals/{mineral_id}', response_model=MineralResponse)
@cache(key='mineral_by_id')
async def mineral_by_id(mineral_id: int, db: DBDep, redis: RedisDep):
    ans = await db.minerals.by_id(
        type_id=mineral_id,
        load_relations=True
    )
    if ans is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Минерал не найден')
    return {
        'id': ans.id,
        'name': ans.name,
        'compact_name': ans.compact_name,
        'description': ans.description,
        'intake': ans.intake,
        'type_id': ans.type_id,
        'type_name': ans.type.name,
    }


@mineral_router_v1.delete('/minerals/{mineral_id}', response_model=Ok)
async def del_mineral(mineral_id: int, db: DBDep, user: UserDep):
    return {'ok': await db.minerals.del_by_id(mineral_id=mineral_id)}


@mineral_router_v1.post('/minerals/new', response_model=Ok)
async def save_new_mineral(new: NewMineral, db: DBDep, user: UserDep):
    return {'ok': await db.minerals.new(
        name=new.name,
        compact_name=new.compact_name,
        description=new.description,
        intake=new.intake,
        type_id=new.type_id,
    )}


@mineral_router_v1.get('/types/', response_model=MultipleMineralTypeResponse)
@cache(key='mineral_types_pagination')
async def mineral_types_pagination(db: DBDep, pagination: PaginationParams, redis: RedisDep):
    types = await db.mineral_types.pagination(
        skip=pagination.skip,
        limit=pagination.limit,
        load_relations=True
    )
    return {'types': [{
        'id': t.id,
        'name': t.name,
        'description': t.description,
        'minerals': [{
            'id': mineral.id,
            'name': mineral.name,
            'compact_name': mineral.compact_name,
            'description': mineral.description,
        } for mineral in t.minerals]
    } for t in types]}


@mineral_router_v1.get('/types/{type_id}', response_model=MineralTypeResponse)
@cache(key='mineral_type_by_id')
async def type_by_id(type_id: int, db: DBDep, redis: RedisDep):
    ans = await db.mineral_types.by_id(
        type_id=type_id,
        load_relations=True
    )
    if ans is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Тип минералов не найден')
    return ans


@mineral_router_v1.delete('/types/{type_id}', response_model=Ok)
async def del_type(type_id: int, db: DBDep, user: UserDep):
    return {'ok': await db.mineral_types.del_by_id(type_id=type_id)}


@mineral_router_v1.post('/types/new', response_model=Ok)
async def save_new_type(new: NewMineralType, db: DBDep, user: UserDep):
    return {'ok': await db.mineral_types.new(
        name=new.name,
        description=new.description,
    )}
