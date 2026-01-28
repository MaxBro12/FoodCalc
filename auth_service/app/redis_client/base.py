from typing import Any
from fastapi import Request
import redis.asyncio as redis

from .exceptions import RedisConnectionError, UnsupportedAnswer, UnsupportedType

from app.settings import settings


class RedisClient:
    def __init__(self, redis_pool: redis.ConnectionPool):
        self.__client = redis.Redis(connection_pool=redis_pool)

        self.__prefix = settings.REDIS_PREFIX
        self.__expire = settings.REDIS_EXPIRE

    def __insert_prefix_key(self, key: str | int) -> str:
        return f'{self.__prefix}_{str(key)}'

    def __parse_ans(self, ans: str | bytes):
        if ans is None:
            return None
        match ans[0]:
            case 'b':
                return True if ans == 'b1' else False
            case 'B':
                return ans[1:]
            case 's':
                return ans[1:]
            case 'i':
                return int(ans[1:])
            case 'f':
                return float(ans[1:])
        raise UnsupportedAnswer(ans)

    def __type_pointer(self, value) -> str:
        t = type(value)
        if t is str:
            return f's{value}'
        elif t is bytes:
            return f'B{value}'
        elif t is int:
            return f'i{value}'
        elif t is float:
            return f'f{value}'
        elif t is bool:
            return 'b1' if value else 'b0'
        raise UnsupportedType(value)

    async def get(self, key: str | int):
        return self.__parse_ans(await self.__client.get(self.__insert_prefix_key(key)))

    async def set(self, key: str, value: Any):
        return await self.__client.set(
            self.__insert_prefix_key(key),
            self.__type_pointer(value),
            ex=self.__expire
        )

    def multiple_keys(self, keys: list[str | int] | tuple[str | int]):
        return f'{self.__prefix}_{":".join(map(str, keys))}'

    async def get_dict(self, key: str) -> dict | None:
        data = await self.__client.hgetall(self.__insert_prefix_key(key))
        if data is None:
            return None
        return {k: self.__parse_ans(v) for k, v in data.items()}

    async def set_dict(self, key: str, data: dict):
        data_to_save = {}
        for k, v in data.items():
            data_to_save[k] = self.__type_pointer(v)
        await self.__client.hset(
            self.__insert_prefix_key(key),
            mapping=data_to_save
        )
