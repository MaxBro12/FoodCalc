from fastapi import APIRouter, Request

from app.core import dispatcher
from app.routers.misc_models import Ok
from app.depends import Token
from .model import Feedback


utils_router_v1 = APIRouter(prefix="/v1/utils", tags=["utils"])


@utils_router_v1.post("/feedback", response_model=Ok)
async def feedback_data(feedback: Feedback, token: Token):
    await dispatcher.send(
        title='Сообщение от пользователя:',
        message=feedback.message,
        level='info',
        logs=f'Пользователь {token.user.name}'
    )
    return {"ok": True}
