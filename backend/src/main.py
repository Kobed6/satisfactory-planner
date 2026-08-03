from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import get_all_items, get_all_recipes, get_search_recipes, to_name
from typing import List
from .models import Item, Recipe
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

@app.get('/search', response_model=List[str])
def search_recipes(input: str):
    return get_search_recipes(input)

@app.get('/solve', response_model=dict)
def solve(final_recipe: str, recipe_list: List[str] | None = None):
    prob_vars = calculate(final_recipe, recipe_list)
    res = {}
    for item_className, var in prob_vars.items():
        res[to_name(item_className)] = var.varValue
    return res