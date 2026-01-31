from fastapi import APIRouter, HTTPException, status, Response
from fastapi.requests import Request

from core.pydantic_misc_models import Ok
from app.services import auth_service
from app.handlers import AuthHandler
from app.depends import DBDep, UserDep
from .models import UserLogin, UserRegister


auth_router_v1 = APIRouter(prefix='/v1/auth', tags=['auth'])


@auth_router_v1.post('/login', response_model=Ok)
async def login(response: Response, user_data: UserLogin):
    return {'ok': await AuthHandler().login(user_data, response)}


@auth_router_v1.post('/refresh', response_model=Ok)
async def refresh(request: Request, response: Response):
    #await auth.refresh(request=request, response=response)
    return {'ok': True}


@auth_router_v1.post('/logout', response_model=Ok)
async def logout(response: Response, user: UserDep):
    return {'ok': await AuthHandler().logout(user=user, response=response)}


@auth_router_v1.post('/register', response_model=Ok)
async def register(user_data: UserRegister):
    return {'ok': await AuthHandler().register(user=user_data)}
