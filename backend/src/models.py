from pydantic import BaseModel

class Item(BaseModel):
    id: int
    className: str
    name: str
    producedIn: str

class Recipe(BaseModel):
    id: int
    name: str
    unlockedBy: str
    duration: int
    producedIn: str
    alternate: bool

class SearchRecipe(BaseModel):
    name: str
    ingredients: str
    products: str

class ResourceInput(BaseModel):
    resource: str
    amount: float

class SolveRequest(BaseModel):
    target_item: str
    final_recipe: str
    inputs: list[ResourceInput]
    recipe_list: list[str] | None = None