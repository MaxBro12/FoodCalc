from fastapi import APIRouter

from .models import Ok, Bans, NewBan
from app.depends import DBDep, RedisDep
from app.routers.decorators.cashe_decor import cache


bans_router_v1 = APIRouter(prefix='/v1/bans', tags=['bans'])


@bans_router_v1.post('', response_model=Ok)
async def add_ban(db: DBDep, data: NewBan):
    return {'ok': await db.bans.new(data.ip, reason=data.reason)}


@bans_router_v1.get('', response_model=Bans)
async def bans(db: DBDep, skip: int = 0, limit: int = 10):
    if skip or limit:
        return {'bans': await db.bans.pagination(skip=skip, limit=limit)}
    return {'bans': await db.bans.all()}


@bans_router_v1.get('/{ip_address}', response_model=Ok)
@cache(key='ban')
async def in_ban(ip_address: str, db: DBDep, redis: RedisDep):
    return {'ok': await db.bans.exists(ip_address)}


@bans_router_v1.delete('/{ip_address}', response_model=Ok)
async def del_ban(ip_address: str, db: DBDep):
    return {'ok': await db.bans.delete_by_ip(ip_address)}
