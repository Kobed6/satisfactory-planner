import os
from dotenv import load_dotenv
import mysql.connector
import pulp
from collections import deque

load_dotenv()

db = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    user=os.getenv('DB_USER'),
    passwd=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
)

def get_extractor_output(extractor, purity):
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

def get_ingredients(db, item: str):
    '''Get ingredients of a recipe using a recipe's in-game name'''
    try:
        query = '''
            SELECT * FROM Ingredients WHERE recipeID =
                (SELECT id FROM Recipes WHERE name=%s)
        '''
        with db.cursor(dictionary=True) as cursor:
            cursor.execute(query, (item,))
            return cursor.fetchall()
    except TypeError as e:
        print(f'{e}\n{item} is not a string')

def get_products(db, item: str):
    '''Get products of a recipe using a recipe's in-game name'''
    try:
        query = '''
            SELECT * FROM Products WHERE recipeID =
                (SELECT id FROM Recipes WHERE name=%s)
        '''
        with db.cursor(dictionary=True) as cursor:
            cursor.execute(query, (item,))
            return cursor.fetchall()
    except TypeError as e:
        print(f'{e}\n{item} is not a string')

def get_origin_recipe(db, item: str):
    '''Get original recipe of an item using the item's in-game name'''
    try:
        with db.cursor(dictionary=True) as cursor:
            query = '''
                SELECT * FROM Recipes WHERE name=%s
            '''
            cursor.execute(query, (item,))
            res = cursor.fetchone()
            if res:
                return res
            else:
                print(f'Warning: get_origin_recipe returning None (item: {item})')
                return None
    except TypeError as e:
        print(f'{e}\n{item} is not a string')

def get_recipes(db, item: str):
    '''Get recipes of an item using its in-game name'''
    try:
        with db.cursor(dictionary=True) as cursor:
            id_query = '''
                SELECT recipeID FROM Products WHERE item =
                    (SELECT className FROM Items WHERE name=%s)
            '''
            cursor.execute(id_query, (item,))

            recipeIDs = []
            for product in cursor:
                recipeIDs.append(product['recipeID'])

            specifiers = ', '.join(['%s'] * len(recipeIDs))
            recipes_query = f'''
                SELECT * FROM Recipes WHERE id IN ({specifiers})
            '''
            cursor.execute(recipes_query, recipeIDs)
            return cursor.fetchall()
    except TypeError as e:
        print(f'{e}\n{item} is not a string')

def get_item(db, item: str):
    '''Get item record of an item using its in-game name'''
    try:
        with db.cursor(dictionary=True) as cursor:
            query = '''
                SELECT * FROM Items WHERE name=%s
            '''
            cursor.execute(query, (item,))
            res = cursor.fetchone()
            if res:
                return res
            else:
                print(f'Warning: get_item returning None (item: {item})')
                return None
    except TypeError as e:
        print(f'{e}\n{item} is not a string')

def get_main_product(db, recipe_name: str):
    '''Get the main product of a recipe using its className'''      # main product is always the first one
    try:
        with db.cursor(dictionary=True) as cursor:
            query = '''
                SELECT * FROM Products WHERE recipeID=
                    (SELECT id FROM Recipes WHERE className=%s)
            '''
            cursor.execute(query, (recipe_name,))
            res = cursor.fetchall()
            if res:
                return res[0]
            else:
                print(f'Warning: get_product returning None (recipe name: {recipe_name})')
                return None
    except TypeError as e:
        print(f'{e}\n{recipe_name} is not a string')

def to_className(db, item: str):
    '''Returns the className of an item using its in-game name'''
    try:
        with db.cursor(dictionary=True) as cursor:
            query = '''
                SELECT className FROM Items WHERE name=%s
            '''
            cursor.execute(query, (item,))
            res = cursor.fetchone()
            if res:
                return res['className']
            else:
                print(f'Warning: to_className returning None (item: {item})')
                return None
    except TypeError as e:
        print(f'{e}\n{item} is not a string')

def to_name(db, className: str):
    '''Returns the in-game name of an item using its className'''
    try:
        with db.cursor(dictionary=True) as cursor:
            query = '''
                SELECT name FROM Items WHERE className=%s
            '''
            cursor.execute(query, (className,))
            res = cursor.fetchone()
            if res:
                return res['name']
            else:
                print(f'Warning: to_name returning None (className: {className})')
                return None
    except TypeError as e:
        print(f'{e}\n{className} is not a string')

def print_output(status, prob_vars):
    print(f'Status: {status}')
    for _, var in prob_vars.items():
        print(f'Number of {var.name}: {var.varValue}')

def calculate(db, item: str):   # maybe dict for node purities (resource: purity)
    '''Returns LpProblem with maximum outputs of each item using base recipes'''
    curr_recipe = get_origin_recipe(db, item)
    item_className = to_className(db, item)

    prob = pulp.LpProblem(f'Maximize_{item_className}', pulp.LpMaximize)
    prob_vars = {}
    prob_vars[item_className] = prob.add_variable(f'{item_className}', lowBound=0, cat='Continuous')
    prob += prob_vars[item_className], f'Total_{item_className}_Output'

    recipes_queue = deque([curr_recipe])
    seen_recipes = set()
    ingredient_products = {}
    # ore_outputs = {}
    while len(recipes_queue) > 0:
        curr_recipe = recipes_queue.popleft()
        curr_recipe_className = curr_recipe['className']
        if curr_recipe_className not in seen_recipes:
            seen_recipes.add(curr_recipe_className)
            curr_recipe_product = get_main_product(db, curr_recipe['className'])
            curr_recipe_product_var = prob_vars[curr_recipe_product['item']]
            ingredients = get_ingredients(db, curr_recipe['name'])

            for ingredient in ingredients:
                item_name = to_name(db, ingredient['item'])
                item_className = ingredient['item']
                item_record = get_item(db, item_name)
                if item_record['producedIn'] == '':     # item is not from an extractor
                    recipes_queue.append(get_origin_recipe(db, item_name))
                    if prob_vars.get(item_className) is None:      # no variable exists for this item, create one
                        prob_vars[item_className] = prob.add_variable(f'{item_className}', lowBound=0, cat='Continuous')
                else:
                    extractor_output = get_extractor_output(item_record['producedIn'], 2)
                    prob_vars[item_className] = prob.add_variable(f'{item_className}', lowBound=0, upBound=extractor_output, cat='Continuous')

                if ingredient_products.get(item_className):
                    ingredient_products[item_className].append((ingredient['amount'] / curr_recipe_product['amount']) * curr_recipe_product_var)
                else:
                    ingredient_products[item_className] = [(ingredient['amount'] / curr_recipe_product['amount']) * curr_recipe_product_var]

    for ingredient, products in ingredient_products.items():
        if len(products) > 1:
            prob += pulp.lpSum(products) == prob_vars[ingredient]
        else:
            prob += products[0] == prob_vars[ingredient]

    solver = pulp.COIN_CMD(msg=False)
    status = prob.solve(solver)
    print_output(pulp.LpStatus[status], prob_vars)
    return prob_vars

calculate(db, 'Computer')