from fastapi import APIRouter
from core.pydantic_misc_models import Ok


utils_router_v1 = APIRouter(prefix="/v1/status", tags=["utils"])


@utils_router_v1.get("/status", response_model=Ok)
async def status():
    return {"ok": True}
