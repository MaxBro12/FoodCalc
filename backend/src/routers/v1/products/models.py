from pydantic import BaseModel


class MineralInProduct(BaseModel):
    id: int
    content: float


class NewProduct(BaseModel):
    id: str
    name: str
    description: str
    minerals: list[MineralInProduct]
    calories_per_100g: float
    proteins_per_100g: float
    fats_per_100g: float
    carbs_per_100g: float
    fiber_per_100g: float
    sugar_per_100g: float


class SearchProduct(BaseModel):
    id_or_name: str


class ProductName(BaseModel):
    id: str
    name: str
    search_index: float


class ProductsNames(BaseModel):
    names: list[ProductName]


class MineralInProductResponse(MineralInProduct):
    name: str
    compact_name: str
    type_id: int


class ProductResponse(BaseModel):
    id: str
    name: str
    description: str
    minerals: list[MineralInProductResponse]
    calories_per_100g: float
    proteins_per_100g: float
    fats_per_100g: float
    carbs_per_100g: float
    fiber_per_100g: float
    sugar_per_100g: float
    added_by_name: str


class MultipleProductsResponse(BaseModel):
    products: list[ProductResponse]
