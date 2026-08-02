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