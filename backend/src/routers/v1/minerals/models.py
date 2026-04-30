from pydantic import BaseModel


class MineralResponse(BaseModel):
    id: int
    name: str
    compact_name: str
    description: str
    daily_value: float
    type_id: int
    type_name: str


class MultipleMineralResponse(BaseModel):
    minerals: list[MineralResponse]


class MineralResponseMini(BaseModel):
    id: int
    name: str
    compact_name: str
    description: str


class MineralTypeResponse(BaseModel):
    id: int
    name: str
    description: str
    minerals: list[MineralResponseMini]


class MultipleMineralTypeResponse(BaseModel):
    types: list[MineralTypeResponse]
