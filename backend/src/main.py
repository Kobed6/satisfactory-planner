from fastapi import FastAPI
from .database import get_all_items, get_all_recipes

app = FastAPI()

@app.get('/items')
def get_items():
    return get_all_items()

@app.get('/recipes')
def get_recipes():
    return get_all_recipes()