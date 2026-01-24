from typing import Annotated, AsyncGenerator

from fastapi import Depends, Request

from app.core.auth import AuthService, TokenData
from .db import DBDep


async def verify_access_token(db: DBDep, request: Request) -> TokenData:
    auth = AuthService(db)
    return await auth.verify_access_token(request)


TokenDep = Annotated[TokenData, Depends(verify_access_token)]


async def auth_service_dep(db: DBDep) -> AsyncGenerator[AuthService, None]:
    yield AuthService(db)


AuthDep = Annotated[AuthService, Depends(auth_service_dep)]
