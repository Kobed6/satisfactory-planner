from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import get_all_items, get_all_recipes, get_search_items, get_search_recipes, to_name
from typing import List
from .models import Item, Recipe, SearchRecipe
from .solver import calculate

app = FastAPI()

origins = [
    'http://localhost:5173'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=['*'],
    allow_headers=['*']
)

@app.get('/items', response_model=List[Item])
def get_items():
    return get_all_items()

@app.get('/recipes', response_model=List[Recipe])
def get_recipes():
    return get_all_recipes()

@app.get('/search-items', response_model=List[str])
def search_items(input: str):
    return get_search_items(input)

@app.get('/search-recipes', response_model=List[SearchRecipe])
def search_recipes(item: str):
    return get_search_recipes(item)

@app.get('/solve', response_model=dict)
def solve(target_item: str, final_recipe: str, recipe_list: List[str] | None = None):
    recipe_vars = calculate(target_item, final_recipe, recipe_list)
    res = {}
    for item_className, var in recipe_vars.items():
        res[to_name(item_className)] = var
    return res