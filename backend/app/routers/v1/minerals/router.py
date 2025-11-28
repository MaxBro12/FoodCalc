from fastapi import APIRouter

from app.database import DB
from app.depends import SessionDep


mineral_router_v1 = APIRouter(prefix='/v1/universe', tags=['minerals and types'])


@mineral_router_v1.get('/minerals/{mineral_id}')
async def mineral_by_id(mineral_id: int, session: SessionDep):
    return {'mineral': await DB.mineral_types.all(session=session)}


@mineral_router_v1.get('/types/{mineral_id}')
async def mineral_types_by_id(mineral_id: int, session: SessionDep):
    return {'types': await DB.mineral_types.all(session=session)}
