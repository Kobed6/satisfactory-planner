from typing import Optional
try:
    from .database import get_ingredients, get_products, get_nonalt_recipe, get_recipe, get_item, to_className, to_name, recipe_name_to_className, recipe_className_to_name, building_className_to_name
except ImportError:
    from database import get_ingredients, get_products, get_nonalt_recipe, get_recipe, get_item, to_className, to_name, recipe_name_to_className, recipe_className_to_name, building_className_to_name
import pulp
from collections import deque

def get_extractor_output(extractor: str, purity: int) -> int:
    """
        Get output of miner or water/oil extractor based on node purity\n
        Purities: 0 = Impure, 1 = Normal, 2 = Pure
    """
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

def get_nonalt_recipes(recipe_name: str) -> list:
    """Returns the chain of non-alternate recipes used to make an item.
    Args:
        item (str): The final output item's className
    """
    curr_recipe = get_recipe(recipe_name)
    recipes = [curr_recipe]
    recipes_queue = deque([curr_recipe])
    seen_recipes = set()

    while len(recipes_queue) > 0:
        curr_recipe = recipes_queue.popleft()

        for ingredient in get_ingredients(curr_recipe['name']):
            item_name = to_name(ingredient['item'])
            ingredient_className = ingredient['item']
            if not get_item(item_name)['isRawResource']:     # item is a raw resource
                nonalt_recipe = get_nonalt_recipe(ingredient_className)
                recipes_queue.append(nonalt_recipe)
                recipes.append(nonalt_recipe)
    return recipes

def convert_output(recipe_vars: dict):
    """Convert from LpVariables which represent how many times a recipe is run to values representing how much of each item is produced
    Args:
        recipe_vars (dictionary[str, LpVariable]): A dictionary mapping recipe classNames to their LpVariables
    Returns:
        A dictionary mapping item classNames to their respective outputs
    """
    outputs = {}
    for recipe_className, var in recipe_vars.items():
        products = get_products(recipe_className_to_name(recipe_className))
        for product in products:
            product_className = product['item']
            outputs[product_className] = outputs.get(product_className, 0) + product['amount'] * var.varValue
    return outputs

def calculate(target_item: str, final_recipe_name: str, inputs: dict, recipes: Optional[list] = None):
    """Calculate a linear problem maximizing runs of recipes
    Args:
        target_item (str): In-game name of the target item
        final_recipe_name (str): In-game name of the target item's recipe
        inputs (dict): A dictionary mapping raw resources (in lowercase) to their respective input amounts
        recipes (list of recipes, optional): A list of recipe records to be used in the calculation
    Returns:
        A tuple containing an LpProblem, the PuLP LpProblem used in the calculation, a dict, which maps item classNames to the amount produced of that item, and a list of \
            item names of products that are not ingredients in the chain
    """
    print(f'\nCALCULATE\ntarget_item: {target_item}\nfinal_recipe_name: {final_recipe_name}\ninputs: {inputs}')
    recipe = get_recipe(final_recipe_name)
    recipe_className = recipe['className']

    prob = pulp.LpProblem(f'Maximize_{recipe_className}', pulp.LpMaximize)
    recipe_vars = {}
    recipe_vars[recipe_className] = prob.add_variable(f'{recipe_className}', lowBound=0, cat='Continuous')
    prob += recipe_vars[recipe_className], f'Total_{recipe_className}_Runs'

    recipe_list = []
    if recipes is None:
        recipe_list = get_nonalt_recipes(recipe['name'])
    else:
        recipe_list = recipes

    seen_recipes = set()
    all_products = {}
    all_ingredients = {}
    for recipe in recipe_list:
        recipe_className = recipe['className']
        recipe_name = recipe['name']

        if recipe_className not in seen_recipes:
            seen_recipes.add(recipe_className)
            if recipe_vars.get(recipe_className) is None:
                recipe_vars[recipe_className] = prob.add_variable(recipe_className, lowBound=0, cat='Continuous')

            r_var = recipe_vars[recipe_className]

            for product in get_products(recipe_name):
                product_item = product['item']
                if all_products.get(product_item) is None:
                    all_products[product_item] = []

                all_products[product_item].append((product['amount'], r_var))

            for ingredient in get_ingredients(recipe_name):
                ingredient_item = ingredient['item']
                if all_ingredients.get(ingredient_item) is None:
                    all_ingredients[ingredient_item] = []

                all_ingredients[ingredient_item].append((ingredient['amount'], r_var))

    all_items = set(all_products) | set(all_ingredients)
    non_ingredient_products = []
    try:
        for item in all_items:
            item_name = to_name(item)
            record = get_item(item_name)
            if record['isRawResource']:          # item is a raw resource
                consumed = pulp.lpSum(amount * recipe_var for amount, recipe_var in all_ingredients[item])
                prob += consumed <= inputs[item_name.lower()]
            else:
                produced = pulp.lpSum(amount * recipe_var for amount, recipe_var in all_products[item])
                if all_ingredients.get(item) is not None:
                    consumed = pulp.lpSum(amount * recipe_var for amount, recipe_var in all_ingredients[item])
                    prob += consumed <= produced
                else:
                    if item_name != target_item:
                        non_ingredient_products.append(item_name)

        solver = pulp.COIN_CMD(msg=False)
        status = prob.solve(solver)
        print(f'Status: {pulp.LpStatus[status]}')
        return (prob, recipe_vars, non_ingredient_products)
    except KeyError as e:
        print(f'Required input missing {e}')
        return None

def calculate_recipes(target_item: str, final_recipe_name: str, inputs: dict, recipes: Optional[list] = None):
    """Determine the amount of each product in the recipe chain
    Args:
        target_item (str): In-game name of the target item
        final_recipe_name (str): In-game name of the target item's recipe
        inputs (dict): A dictionary mapping raw resources (in lowercase) to their respective input amounts
        recipes (list of recipes, optional): A list of recipe records to be used in the calculation
    Returns:
        A list of tuples containing a str, the recipe name, a list[str], representing ingredient(s) per minute, a list[str], representing product(s) per minute, \
            and a str, the buildings needed
    """
    recipe_vars = calculate(target_item, final_recipe_name, inputs, recipes)[1]
    output = []
    for recipe, var in recipe_vars.items():
        recipe_name = recipe_className_to_name(recipe)
        times_run = var.varValue
        print(recipe, times_run)
        ingredient_strings = []
        product_strings = []
        buildings_string = ''

        for ingredient in get_ingredients(recipe_name):
            ingredient_strings.append(f'{to_name(ingredient['item'])} ({ingredient['amountPerMin']} per minute)')

        for product in get_products(recipe_name):
            product_strings.append(f'{to_name(product['item'])} ({product['amountPerMin']} per minute)')

        recipe = get_recipe(recipe_name)
        buildings_needed = (times_run * recipe['duration']) / 60
        partial_needed = buildings_needed % 1
        if partial_needed == 0:
            buildings_string = f'{int(buildings_needed)} {building_className_to_name(recipe['producedIn'])}(s) at 100%'
        else:
            building = building_className_to_name(recipe['producedIn'])
            buildings_string = f'{int(buildings_needed)} {building}(s) at 100%, 1 {building} at {round(partial_needed * 100, 4)}%'

        new_tuple = (recipe_name, ingredient_strings, product_strings, buildings_string)
        output.append(new_tuple)
    return output

def calculate_items(target_item: str, final_recipe_name: str, inputs: dict, recipes: Optional[list] = None):
    """Determine the amount of each product in the recipe chain
    Args:
        target_item (str): In-game name of the target item
        final_recipe_name (str): In-game name of the target item's recipe
        inputs (dict): A dictionary mapping raw resources (in lowercase) to their respective input amounts
        recipes (list of recipes, optional): A list of recipe records to be used in the calculation
    Returns:
        A dictionary mapping item names to values representing output of that item
    """
    recipe_vars = calculate(target_item, final_recipe_name, inputs, recipes)[1]
    return(convert_output(recipe_vars))

def calculate_extraneous(target_item: str, final_recipe_name: str, inputs: dict, recipes: Optional[list] = None):
    """Determine the extraneous outputs in the recipe chain (if any)
    Args:
        target_item (str): In-game name of the target item
        final_recipe_name (str): In-game name of the target item's recipe
        inputs (dict): A dictionary mapping raw resources (in lowercase) to their respective input amounts
        recipes (list of recipes, optional): A list of recipe records to be used in the calculation
    Returns:
        A dictionary mapping item names to values representing extraneous output of that item
    """
    prob, recipe_vars, non_ingredient_products = calculate(target_item, final_recipe_name, inputs, recipes)
    prev_values = convert_output(recipe_vars)
    extraneous_outputs = {}
    prob.sense = pulp.LpMinimize
    target_var = recipe_vars[recipe_name_to_className(final_recipe_name)]
    prob += target_var == target_var.varValue
    prob.solve()
    new_values = convert_output(recipe_vars)

    for item_className, amount in prev_values.items():
        diff = amount - new_values[item_className]
        if diff > 0:
            extraneous_outputs[to_name(item_className)] = round(diff, 5)

    for item_name in non_ingredient_products:
        extraneous_outputs[item_name] = new_values[to_className(item_name)]
    return extraneous_outputs

print(calculate_recipes('Stator', 'Stator', {'iron ore': 120, 'copper ore': 120, 'coal': 120}))