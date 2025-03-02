from fastapi import APIRouter
from settings import VITAMINS_API_PATH, VITAMINS_TAGS


router = APIRouter(prefix=VITAMINS_API_PATH, tags=VITAMINS_TAGS)


@router.get("/all")
async def get_vitamins():
    return {'msg': 'test'}


@router.get('/info')
async def get_vitamin_info():
    return {'msg': 'test'}
