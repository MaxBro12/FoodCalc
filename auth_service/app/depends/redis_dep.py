from typing import AsyncGenerator, Annotated

from fastapi import Depends, Request

from app.redis_client import RedisClient


async def redis_dep(request: Request) -> AsyncGenerator[RedisClient, None]:
    yield request.app.state.redis


RedisDep = Annotated[RedisClient, Depends(redis_dep)]
