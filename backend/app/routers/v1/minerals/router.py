from fastapi import APIRouter, HTTPException, status

from app.database import DB
from app.depends import SessionDep
from app.depends.pagination import PaginationParams
from app.routers.misc_models import Ok
from app.depends import TokenDep
from app.routers.decorators import admin_access
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
async def minerals_pagination(session: SessionDep, pagination: PaginationParams):
    minerals = await DB.minerals.pagination(
        skip=pagination.skip,
        limit=pagination.limit,
        session=session,
        load_relations=True
    )
    return {'minerals': [{
        'id': mineral.id,
        'name': mineral.name,
        'description': mineral.description,
        'intake': mineral.intake,
        'type_id': mineral.type_id,
        'type_name': mineral.type.name
    } for mineral in minerals]}


@mineral_router_v1.get('/minerals/{mineral_id}', response_model=MineralResponse)
async def mineral_by_id(mineral_id: int, session: SessionDep):
    ans = await DB.minerals.by_id(
        type_id=mineral_id,
        session=session,
        load_relations=True
    )
    if ans is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Минерал не найден')
    return {
        'id': ans.id,
        'name': ans.name,
        'description': ans.description,
        'intake': ans.intake,
        'type_id': ans.type_id,
        'type_name': ans.type.name,
    }


@admin_access
@mineral_router_v1.delete('/minerals/{mineral_id}', response_model=Ok)
async def del_mineral(mineral_id: int, session: SessionDep, token: TokenDep):
    return {'ok': await DB.minerals.del_by_id(mineral_id=mineral_id, session=session)}


@admin_access
@mineral_router_v1.post('/minerals/new', response_model=Ok)
async def save_new_mineral(new: NewMineral, session: SessionDep, token: TokenDep):
    return {'ok': await DB.minerals.new(
        name=new.name,
        description=new.description,
        intake=new.intake,
        type_id=new.type_id,
        session=session,
    )}


@mineral_router_v1.get('/types/', response_model=MultipleMineralTypeResponse)
async def mineral_types_pagination(session: SessionDep, pagination: PaginationParams):
    types = await DB.mineral_types.pagination(
        skip=pagination.skip,
        limit=pagination.limit,
        session=session,
        load_relations=True
    )
    return {'types': [{
        'id': t.id,
        'name': t.name,
        'description': t.description,
        'minerals': [{
            'id': mineral.id,
            'name': mineral.name,
            'description': mineral.description,
        } for mineral in t.minerals]
    } for t in types]}


@mineral_router_v1.get('/types/{type_id}', response_model=MineralTypeResponse)
async def type_by_id(type_id: int, session: SessionDep):
    ans = await DB.mineral_types.by_id(
        type_id=type_id,
        session=session,
        load_relations=True
    )
    if ans is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Тип минералов не найден')
    return ans


@admin_access
@mineral_router_v1.delete('/types/{type_id}', response_model=Ok)
async def del_type(type_id: int, session: SessionDep, token: TokenDep):
    return {'ok': await DB.mineral_types.del_by_id(type_id=type_id, session=session)}


@admin_access
@mineral_router_v1.post('/types/new', response_model=Ok)
async def save_new_type(new: NewMineralType, session: SessionDep, token: TokenDep):
    return {'ok': await DB.mineral_types.new(
        name=new.name,
        description=new.description,
        session=session,
    )}
