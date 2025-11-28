from fastapi import APIRouter

from app.depends import SessionDep, PaginationParams
from app.routers.misc_models import Ok
from app.database.repo import DB


products_router_v1 = APIRouter(prefix='/v1/products', tags=['products'])


@products_router_v1.get('/')
async def minerals_pagination(session: SessionDep, pagination: PaginationParams):
    return {'products': await DB.minerals.pagination(
        skip=pagination.skip,
        limit=pagination.limit,
        session=session,
        load_relations=True
    )}


@products_router_v1.get('/{mineral_id}')
async def mineral_by_id(mineral_id: int, session: SessionDep):
    return {'mineral': await DB.minerals.by_id(
        type_id=mineral_id,
        session=session,
        load_relations=True
    )}


@products_router_v1.post('/new', response_model=Ok)
async def save_new_mineral(session: SessionDep):
    return ...