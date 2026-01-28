try:
    import app
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))


from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException, Request, status
import redis.asyncio as redis
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.core.debug import logger
from app.database import init_db
from app.redis_client import RedisClient

from app.routers.v1 import auth_router_v1
from app.depends import DBDep

from app.settings import settings


redis_c = redis.ConnectionPool.from_url(settings.REDIS_URL, decode_responses=True)


async def auto_update():
    logger.log('> Daily auto update', 'info')
    pass


# ? Планеровщик
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Запускаем бд
    await init_db()

    # Подключаю Redis
    app.state.redis = RedisClient(redis_pool=redis_c)

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


@app.middleware('http')
async def check_access_code(request: Request, call_next):
    if not settings.DEBUG and request.headers.get('X-Access-Code') != settings.ACCESS_CODE:
        #if request.client is not None:
        #    await db.bans.new(ip_address=request.client.host, reason='Invalid access code')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Goodbye!'
        )
    response = await call_next(request)
    return response


if __name__ == "__main__":
    try:
        uvicorn.run(app, host=settings.HOST, port=settings.PORT)
    except Exception as e:
        logger.log(e, 'crit')
