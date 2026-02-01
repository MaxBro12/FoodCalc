try:
    import app
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))


import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException, Request, status
import redis.asyncio as redis
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.database import init_db, new_session
from core.redis_client import RedisClient
from core.fast_routers import utils_router_v1

from app.routers.v1 import auth_router_v1, users_router_v1
from app.database.repo import DataBase

from app.settings import settings


redis_c = redis.ConnectionPool.from_url(settings.REDIS_URL, decode_responses=True)


async def auto_update():
    # Автоматическое обновление раз в день
    logging.info('> Daily auto update')
    async with new_session() as session:
        await DataBase(session).bans.del_old_bans()
    pass


# ? Планеровщик
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаем бд
    await init_db()

    # Добавляем редис
    app.state.redis = RedisClient(
        redis_pool=redis_c,
        prefix=settings.REDIS_PREFIX,
        expire=settings.REDIS_EXPIRE
    )

    # Автообновление
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        auto_update,
        trigger=CronTrigger(hour=12, minute=00),  # Каждый день в 12:00 мск
        timezone="UTC"
    )
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(
    name='Auth Service',
    description='Union Authentication Service',
    version='0.0.1',
    lifespan=lifespan,
)

app.include_router(auth_router_v1)
app.include_router(users_router_v1)
app.include_router(utils_router_v1)


@app.middleware('http')
async def check_access_code(request: Request, call_next):
    """Middleware для проверки access code. Без него доступ к API не будет."""
    if not settings.DEBUG and request.headers.get('X-Access-Code') != settings.ACCESS_CODE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Goodbye!'
        )
    return await call_next(request)


if __name__ == "__main__":
    try:
        uvicorn.run(app, host=settings.HOST, port=settings.PORT)
    except Exception as e:
        logging.critical(e)
