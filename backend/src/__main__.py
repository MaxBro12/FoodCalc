try:
    import src
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))


from contextlib import asynccontextmanager

import uvicorn
import redis.asyncio as redis
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from core.redis_client import RedisClient
from core.fast_middlewares import blocker_check
from src.routers import auth_router_v1, minerals_router_v1, products_router_v1, utils_router_v1
from src.database import init_db
from src.services import blocklist_service

from src.settings import settings


redis_c = redis.ConnectionPool.from_url(settings.REDIS_URL, decode_responses=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Инициализация базы данных
    await init_db()

    # Подключаем Redis
    app.state.redis = RedisClient(
        redis_pool=redis_c,
        prefix=settings.REDIS_PREFIX,
        expire=settings.REDIS_EXPIRE
    )
    yield


if settings.DEBUG:
    app = FastAPI(
        title='Food app backend',
        description='Special api for food app',
        version='0.2.0',
        lifespan=lifespan
    )
else:
    app = FastAPI(
        title='Food app backend',
        description='Special api for food app',
        version='0.2.0',
        lifespan=lifespan,
        docs_url=None,
        redoc_url=None,
        openapi_url=None
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.FRONTEND_URL.split(','),
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'DELETE'],
    allow_headers=["*"],
)

app.include_router(auth_router_v1)
app.include_router(minerals_router_v1)
app.include_router(products_router_v1)
app.include_router(utils_router_v1)


@app.middleware('http')
async def blocker(request: Request, call_next):
    # Запускаем blocker_check для проверки бана и недопустимых эндпоинтов
    await blocker_check(
        request=request,
        app=app,
        blocklist_service=blocklist_service,
        settings=settings,
        redis_client=RedisClient(
            redis_pool=redis_c,
            prefix=settings.REDIS_PREFIX,
            expire=settings.REDIS_EXPIRE
        ),
        exceptions_routes=[
            '/.env'
        ],
    )
    return await call_next(request)


if __name__ == '__main__':
    uvicorn.run(app=app, host=settings.HOST, port=settings.PORT)
