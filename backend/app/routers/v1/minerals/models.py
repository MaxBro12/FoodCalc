from pydantic import BaseModel


class NewMineral(BaseModel):
    name: str
    description: str
    intake: float
    type_id: int


class NewMineralType(BaseModel):
    name: str
    description: str
    intake: float
    type_id: int


class Mineral(BaseModel):
    id: int
    name: str
    description: str
    intake: float
    type_id: int


class MineralsResp(BaseModel):
    minerals: list[Mineral]


class MineralResp(BaseModel):
    mineral: Mineral


class MineralType(BaseModel):
    id: int
    name: str
    description: str


class MineralTypesResp(BaseModel):
    types: list[MineralType]


class MineralTypeResp(BaseModel):
    type: MineralType