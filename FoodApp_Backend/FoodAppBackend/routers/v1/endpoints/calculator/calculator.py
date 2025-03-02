from fastapi import APIRouter
from settings import CALCULATOR_API_PATH, CALCULATOR_TAGS


router = APIRouter(prefix=CALCULATOR_API_PATH, tags=CALCULATOR_TAGS)


@router.get("/all")
async def get_calc_calories():
    return {'msg': 'test'}


@router.get('/info')
async def get_vitamin_info():
    return {'msg': 'test'}
