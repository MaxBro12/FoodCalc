from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import init_db
from app.routers.v1 import auth_router_v1, mineral_router_v1, products_router_v1
from app.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title='Food app backend',
    description='Special api for food app',
    version='0.1.0',
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'DELETE'],
    allow_headers=["*"],
)

app.include_router(auth_router_v1)
app.include_router(mineral_router_v1)
app.include_router(products_router_v1)


if __name__ == '__main__':
    uvicorn.run(app=app, host='0.0.0.0', port=settings.port)
