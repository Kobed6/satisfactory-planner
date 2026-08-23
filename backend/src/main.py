from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import get_all_items, get_all_recipes, get_search_items, get_search_recipes, to_name, search_raw_resources
from typing import List
from .models import Item, Recipe, SearchRecipe, SolveRequest
from .solver import calculate_recipes, calculate_items, calculate_extraneous

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

@app.get('/search-resources', response_model=List[str])
def search_resources(input: str):
    return search_raw_resources(input)

@app.post('/solve/recipes', response_model=List)
def solveItems(request: SolveRequest):
    input_dict = {}
    for i in request.inputs:
        input_dict[i.resource] = i.amount
    return(calculate_recipes(request.target_item, request.final_recipe, input_dict, request.recipe_list))

@app.post('/solve/items', response_model=dict)
def solveItems(request: SolveRequest):
    input_dict = {}
    for i in request.inputs:
        input_dict[i.resource] = i.amount
    return(calculate_items(request.target_item, request.final_recipe, input_dict, request.recipe_list))

@app.post('/solve/extraneous', response_model=dict)
def solveExtraneous(request: SolveRequest):
    input_dict = {}
    for i in request.inputs:
        input_dict[i.resource] = i.amount
    return(calculate_extraneous(request.target_item, request.final_recipe, input_dict, request.recipe_list))