try:
    import app
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))


from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import redis.asyncio as redis

from app.database.init_db import init_db
from app.routers.v1 import auth_router_v1, mineral_router_v1, products_router_v1, utils_router_v1
from app.services import blocklist_service
from core.redis_client import RedisClient

from app.settings import settings


redis_c = redis.ConnectionPool.from_url(settings.REDIS_URL, decode_responses=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()

    app.state.redis = RedisClient(
        redis_pool=redis_c,
        prefix=settings.REDIS_PREFIX,
        expire=settings.REDIS_EXPIRE
    )
    yield


app = FastAPI(
    title='Food app backend',
    description='Special api for food app',
    version='0.1.0',
    lifespan=lifespan
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.FRONTEND_URL.split(','),
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'DELETE'],
    allow_headers=["*"],
)

app.include_router(auth_router_v1)
app.include_router(mineral_router_v1)
app.include_router(products_router_v1)
app.include_router(utils_router_v1)


@app.middleware('http')
async def blocker(request: Request, call_next):
    # Проверяем в бане ли пользователь
    if await blocklist_service.in_ban(request.client.host, RedisClient(
        redis_pool=redis_c,
        prefix=settings.REDIS_PREFIX,
        expire=settings.REDIS_EXPIRE
    )):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )
    # Проверяем не ведет ли эндпойнт в никуда
    exceptions_routes = [ # список эндпоинтов, которые сразу получают бан
        '/.env',
    ]
    if not settings.DEBUG:
        exceptions_routes.extend([
            '/openapi.json',
            '/docs',
            '/redoc',
            '/swagger',
        ])
    routes = tuple([i.path.split('{')[0] for i in app.routes if i not in exceptions_routes])
    if not request.url.path.startswith(routes):
        await blocklist_service.ban(
            ip=request.client.host,
            reason='FoodApp > Endpoint not found',
            duration_days=3,
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )
    response = await call_next(request)
    return response


if __name__ == '__main__':
    uvicorn.run(app=app, host=settings.HOST, port=settings.PORT)
