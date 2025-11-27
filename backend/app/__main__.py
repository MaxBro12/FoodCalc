from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.database import init_db
from app.routers.v1 import auth_router_v1


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title='Food app backend',
    description='Special api for food app',
    version='0.1.0',
)
app.include_router(auth_router_v1)
