from pydantic import BaseModel


class NewMineral(BaseModel):
    name: str
    description: str
    intake: float
    type_id: int


class MineralResponse(BaseModel):
    id: int
    name: str
    description: str
    intake: float
    type_id: int


class MultipleMineralResponse(BaseModel):
    minerals: list[MineralResponse]


class NewMineralType(BaseModel):
    name: str
    description: str


class MineralTypeResponse(BaseModel):
    id: int
    name: str
    description: str


class MultipleMineralTypeResponse(BaseModel):
    types: list[MineralTypeResponse]
