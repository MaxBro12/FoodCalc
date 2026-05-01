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


class UpdateProduct(BaseModel):
    name: str | None = None
    description: str | None = None
    minerals: list[MineralInProduct] | None = None
    calories_per_100g: float | None = None
    proteins_per_100g: float | None = None
    fats_per_100g: float | None = None
    carbs_per_100g: float | None = None
    fiber_per_100g: float | None = None
    sugar_per_100g: float | None = None
    is_verified: bool | None = None


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
    likes: int
    search_index: float
    created_at: str
    updated_at: str
    added_by: str


class MultipleProductsResponse(BaseModel):
    products: list[ProductResponse]
