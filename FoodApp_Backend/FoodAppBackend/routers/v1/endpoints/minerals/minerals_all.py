from fastapi import APIRouter
from settings import MINERALS_API_PATH, MINERALS_TAGS


router = APIRouter(prefix=MINERALS_API_PATH, tags=MINERALS_TAGS)


@router.get("/all")
async def get_minerals():
    return {'msg': 'test'}


@router.get('/info')
async def get_mineral_info():
    return {'msg': 'test'}
