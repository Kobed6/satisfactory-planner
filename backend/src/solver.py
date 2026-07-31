from typing import Optional
try:
    from .database import get_ingredients, get_products, get_nonalt_recipe, get_recipes, get_item, get_main_product, to_className, to_name
except ImportError:
    from database import get_ingredients, get_products, get_nonalt_recipe, get_recipes, get_item, get_main_product, to_className, to_name
import pulp
from collections import deque

def get_extractor_output(extractor, purity) -> int:
    '''
        Get output of miner or water/oil extractor based on node purity\n
        Purities: 0 = Impure, 1 = Normal, 2 = Pure
    '''
    match extractor:
        case 'Desc_MinerMk1_C' | 'Desc_FrackingSmasher_C':
            if purity == 0:
                return 30
            elif purity == 1:
                return 60
            elif purity == 2:
                return 120
        case 'Desc_MinerMk2_C' | 'Desc_OilPump_C':
            if purity == 0:
                return 60
            elif purity == 1:
                return 120
            elif purity == 2:
                return 240
        case 'Desc_MinerMk3_C':
            if purity == 0:
                return 120
            elif purity == 1:
                return 240
            elif purity == 2:
                return 480
        case 'Desc_WaterPump_C':
            return 120
        case _:
            return 0

def get_nonalt_recipes(item: str) -> list:
    curr_recipe = get_nonalt_recipe(item)
    recipes = [curr_recipe]
    recipes_queue = deque([curr_recipe])
    seen_recipes = set()

    while len(recipes_queue) > 0:
        curr_recipe = recipes_queue.popleft()
        curr_recipe_className = curr_recipe['className']
        if curr_recipe_className not in seen_recipes:
            seen_recipes.add(curr_recipe_className)

            for ingredient in get_ingredients(curr_recipe['name']):
                item_name = to_name(ingredient['item'])
                if get_item(item_name)['producedIn'] == '':     # item is not from an extractor
                    recipes_queue.append(get_nonalt_recipe(item_name))
                    recipes.append(get_nonalt_recipe(item_name))
    return recipes

def print_output(status, prob_vars):
    print(f'Status: {status}')
    for _, var in prob_vars.items():
        print(f'Number of {var.name}: {var.varValue}')

def calculate(item: str, recipes: Optional[list] = None):
    '''Returns LpProblem with maximum outputs of each item using base recipes'''
    item_className = to_className(item)

    prob = pulp.LpProblem(f'Maximize_{item_className}', pulp.LpMaximize)
    prob_vars = {}
    prob_vars[item_className] = prob.add_variable(f'{item_className}', lowBound=0, cat='Continuous')
    prob += prob_vars[item_className], f'Total_{item_className}_Output'

    recipe_list = []
    if recipes is None:
        recipe_list = get_nonalt_recipes(item)
    else:
        recipe_list = recipes

    seen_recipes = set()
    ingredient_products = {}
    # ore_outputs = {}
    for recipe in recipe_list:
        recipe_className = recipe['className']
        if recipe_className not in seen_recipes:
            seen_recipes.add(recipe_className)
            recipe_product = get_main_product(recipe['className'])
            recipe_product_var = prob_vars[recipe_product['item']]
            ingredients = get_ingredients(recipe['name'])

            for ingredient in ingredients:
                item_name = to_name(ingredient['item'])
                item_className = ingredient['item']
                item_record = get_item(item_name)
                if item_record['producedIn'] == '':     # item is not from an extractor
                    if prob_vars.get(item_className) is None:      # no variable exists for this item, create one
                        prob_vars[item_className] = prob.add_variable(f'{item_className}', lowBound=0, cat='Continuous')
                else:
                    if prob_vars.get(item_className) is None:      # no variable exists for this item, create one
                        extractor_output = get_extractor_output(item_record['producedIn'], 2)
                        prob_vars[item_className] = prob.add_variable(f'{item_className}', lowBound=0, upBound=extractor_output, cat='Continuous')

                if ingredient_products.get(item_className):
                    ingredient_products[item_className].append((ingredient['amount'] / recipe_product['amount']) * recipe_product_var)
                else:
                    ingredient_products[item_className] = [(ingredient['amount'] / recipe_product['amount']) * recipe_product_var]

    for ingredient, products in ingredient_products.items():
        if len(products) > 1:
            prob += pulp.lpSum(products) == prob_vars[ingredient]
        else:
            prob += products[0] == prob_vars[ingredient]

    solver = pulp.COIN_CMD(msg=False)
    status = prob.solve(solver)
    print_output(pulp.LpStatus[status], prob_vars)
    return prob_vars

