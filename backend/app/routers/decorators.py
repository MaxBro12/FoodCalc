from functools import wraps

from fastapi import HTTPException, status

from app.depends import Token


def admin_access(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        user = kwargs.get('token')
        if type(user) == Token:
            return await func(*args, **kwargs)
        if user is None:
            for arg in args:
                if type(arg) == Token:
                    if arg.user.is_admin:
                        return await func(args, kwargs)
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return wrapper
