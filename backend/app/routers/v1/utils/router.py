from typing import Annotated, Union
from fastapi import APIRouter, Request, Cookie, Response

#from app.core import dispatcher
from app.depends import UserDep
from .model import Feedback
from core.pydantic_misc_models import Ok


utils_router_v1 = APIRouter(prefix="/v1/utils", tags=["utils"])


@utils_router_v1.post("/feedback", response_model=Ok)
async def feedback_data(feedback: Feedback): # , token: TokenDep
    #await dispatcher.send(
    #    title=f'Сообщение от пользователя {token.user.name}',
    #    message=feedback.message,
    #    level='info',
    #    logs=f'Пользователь {token.user.name}'
    #)
    return {"ok": True}


@utils_router_v1.post('/status')
async def get_status(user: UserDep): # , token: TokenDep
    return {"ok": True}
