from fastapi import APIRouter

from app.database import DB
from app.depends import SessionDep
from app.depends.pagination import PaginationParams
from app.routers.v1.minerals.models import NewMineral, NewMineralType, MineralsResp, MineralResp, MineralTypesResp, \
    MineralTypeResp
from app.routers.misc_models import Ok

mineral_router_v1 = APIRouter(prefix='/v1/universe', tags=['minerals and types'])


@mineral_router_v1.get('/minerals/', response_model=MineralsResp)
async def minerals_pagination(session: SessionDep, pagination: PaginationParams):
    return {'minerals': await DB.minerals.pagination(
        skip=pagination.skip,
        limit=pagination.limit,
        session=session,
        load_relations=True
    )}


@mineral_router_v1.get('/minerals/{mineral_id}', response_model=MineralResp)
async def mineral_by_id(mineral_id: int, session: SessionDep):
    return {'mineral': await DB.minerals.by_id(
        type_id=mineral_id,
        session=session,
        load_relations=True
    )}


@mineral_router_v1.post('/new_mineral', response_model=Ok)
async def save_new_mineral(new: NewMineral, session: SessionDep):
    return {'ok': await DB.minerals.new(
        name=new.name,
        description=new.description,
        intake=new.intake,
        type_id=new.type_id,
        session=session,
    )}


@mineral_router_v1.get('/types/', response_model=MineralTypesResp)
async def mineral_types_pagination(session: SessionDep, pagination: PaginationParams):
    return {'types': await DB.mineral_types.pagination(
        skip=pagination.skip,
        limit=pagination.limit,
        session=session,
        load_relations=True
    )}


@mineral_router_v1.get('/types/{type_id}', response_model=MineralTypeResp)
async def mineral_by_id(type_id: int, session: SessionDep):
    return {'type': await DB.mineral_types.by_id(
        type_id=type_id,
        session=session,
        load_relations=True
    )}


@mineral_router_v1.post('/new_mineral_type', response_model=Ok)
async def save_new_mineral(new: NewMineralType, session: SessionDep):
    return {'ok': await DB.mineral_types.new(
        name=new.name,
        description=new.description,
        session=session,
    )}
