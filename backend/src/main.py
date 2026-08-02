from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import get_all_items, get_all_recipes, get_search_recipes
from typing import List
from .models import Item, Recipe

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