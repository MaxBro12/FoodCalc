from fastapi import APIRouter, HTTPException, status

from .models import Ok, Bans, NewBan
from app.depends import DBDep
from core.fast_decorators import cache
from core.redis_client import RedisDep


bans_router_v1 = APIRouter(prefix='/v1/bans', tags=['bans'])


@bans_router_v1.post('', response_model=Ok)
async def add_ban(db: DBDep, data: NewBan, redis: RedisDep):
    if len(data.ip.split('.')) != 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid IP address'
        )
    if await db.bans.exists(data.ip):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='IP address already in ban'
        )
    db_ans = await db.bans.new(ip_address=data.ip, reason=data.reason)
    if db_ans:
        await redis.delete(f'in_ban:ip_address:{data.ip}')
    return {'ok': db_ans}


@bans_router_v1.get('', response_model=Bans)
async def bans(db: DBDep, skip: int = 0, limit: int = 10):
    if skip or limit:
        return {'bans': await db.bans.pagination(skip=skip, limit=limit)}
    return {'bans': await db.bans.all()}


@bans_router_v1.get('/{ip_address}', response_model=Ok)
@cache(key='in_ban', expire=21600)
async def in_ban(ip_address: str, db: DBDep, redis: RedisDep):
    if len(ip_address.split('.')) != 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid IP address'
        )
    return {'ok': await db.bans.exists(ip_address)}


@bans_router_v1.delete('/{ip_address}', response_model=Ok)
async def del_ban(ip_address: str, db: DBDep, redis: RedisDep):
    await redis.delete(f'in_ban:ip_address:{ip_address}')
    return {'ok': await db.bans.delete_by_ip(ip_address)}
