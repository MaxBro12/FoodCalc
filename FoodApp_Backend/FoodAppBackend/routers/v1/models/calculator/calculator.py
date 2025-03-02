from pydantic import BaseModel
from typing import Literal
from enum import Enum


class ActivityLevel(float, Enum):
    sedentary = 1.2
    light = 1.375
    moderate = 1.55
    active = 1.725
    very_active = 1.9


class CalcCaloriesRequest(BaseModel):
    weight: float
    height: int
    age: int
    man: bool
    activity_level: float


class CalcPFCRequest(BaseModel):
    calories: int
    target: Literal["gain", "maintain", "loose"]
