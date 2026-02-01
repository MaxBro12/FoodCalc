from time import time
from typing import Callable
from functools import wraps

from pydantic import BaseModel
from dataclasses import is_dataclass, asdict


def cache(key: str, expire: int = 1800): # 30 минут
    """Кэширование результатов эндпоинта. Для работы в эндпойнте требуется redis: RedisDep"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            redis = kwargs['redis']
            if redis is None:
                return await func(*args, **kwargs)

            keys = ''
            for k, v in kwargs.items():
                if k in ('redis', 'db', 'session', 'token', 'request', 'response', 'exp', 'key'):
                    continue
                keys += f'{k}:{v}'

            r_ans = await redis.get_dict(f'{key}:{keys}')
            if r_ans.get('exp') and time() < r_ans['exp']:
                return r_ans

            ans = await func(*args, **kwargs)
            if is_dataclass(ans):
                ans = asdict(ans)
            elif isinstance(ans, BaseModel):
                ans = ans.model_dump()
            ans['exp'] = time() + expire

            await redis.set_dict(f'{key}:{keys}', ans)
            return ans
        return wrapper
    return decorator
