from typing import Annotated

from fastapi import Depends, Request, Response

from src.handlers.auth import auth_handler, User


async def verify_token(request: Request, response: Response) -> User:
    return await auth_handler.verify_token(request, response)


UserDep = Annotated[User, Depends(verify_token)]
