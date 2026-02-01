from typing import Annotated, Union
from fastapi import APIRouter, Request, Cookie, Response

#from app.core import dispatcher
from app.depends import UserDep
from .model import Feedback
from core.pydantic_misc_models import Ok
from core.fast_routers import utils_router_v1


@utils_router_v1.post("/feedback", response_model=Ok)
async def feedback_data(feedback: Feedback): # , token: TokenDep
    #await dispatcher.send(
    #    title=f'Сообщение от пользователя {token.user.name}',
    #    message=feedback.message,
    #    level='info',
    #    logs=f'Пользователь {token.user.name}'
    #)
    return {"ok": True}
