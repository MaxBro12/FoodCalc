from functools import wraps

from fastapi import HTTPException, status

from app.depends import Token


def admin_access(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        for arg in args:
            if type(arg) == Token:
                if arg.user.is_admin:
                    await func(args, kwargs)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return wrapper
