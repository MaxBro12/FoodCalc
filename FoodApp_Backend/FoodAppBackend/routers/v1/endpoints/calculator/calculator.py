from fastapi import APIRouter
from ...models.calculator import CalcCaloriesRequest, CalcPFCRequest
from settings import CALCULATOR_API_PATH, CALCULATOR_TAGS


router = APIRouter(prefix=CALCULATOR_API_PATH, tags=CALCULATOR_TAGS)


@router.post("/calc_calories_normal")
async def post_calc_calories_normal(calc_data: CalcCaloriesRequest):
    if calc_data.man:
        normal = (88.36 + (13.4 * calc_data.weight) + (4.8 * calc_data.height) - (5.7 * calc_data.age)) * calc_data.activity_level
    else:
        normal = (447.6 + (9.2 * calc_data.weight) + (3.1 * calc_data.height) - (4.3 * calc_data.age)) * calc_data.activity_level
    return {'loose': normal * 0.85, 'normal': normal, 'gain': normal * 1.15}


@router.post('/info')
async def post_calc_pfc(calc_data: CalcPFCRequest):
    if calc_data.target == 'loose':
        return {
            'protein': calc_data.calories * 0.4 / 4,
            'fat': calc_data.calories * 0.3 / 9,
            'carbohydrates': calc_data.calories * 0.3 / 4,
        }
    elif calc_data.target == 'maintain':
        return {
            'protein': calc_data.calories * 0.3 / 4,
            'fat': calc_data.calories * 0.3 / 9,
            'carbohydrates': calc_data.calories * 0.4 / 4,
        }
    elif calc_data.target == 'gain':
        return {
            'protein': calc_data.calories * 0.3 / 4,
            'fat': calc_data.calories * 0.2 / 9,
            'carbohydrates': calc_data.calories * 0.5 / 4,
        }
