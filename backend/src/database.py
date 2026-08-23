import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

db = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    user=os.getenv('DB_USER'),
    passwd=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
)

def get_ingredients(recipe_name: str):
    """Get ingredients of a recipe using a recipe's in-game name"""
    try:
        query = """
            SELECT * FROM Ingredients WHERE recipeID =
                (SELECT id FROM Recipes WHERE name=%s)
        """
        with db.cursor(dictionary=True) as cursor:
            cursor.execute(query, (recipe_name,))
            return cursor.fetchall()
    except TypeError as e:
        print(f'{e}\n{recipe_name} is not a string')

def get_products(recipe_name: str):
    """Get products of a recipe using a recipe's in-game name"""
    try:
        query = """
            SELECT * FROM Products WHERE recipeID =
                (SELECT id FROM Recipes WHERE name=%s)
        """
        with db.cursor(dictionary=True) as cursor:
            cursor.execute(query, (recipe_name,))
            return cursor.fetchall()
    except TypeError as e:
        print(f'{e}\n{recipe_name} is not a string')

def get_recipes(item_className: str):
    """Get recipes of an item using its className"""
    try:
        with db.cursor(dictionary=True) as cursor:
            id_query = """
                SELECT recipeID FROM Products WHERE item = %s
            """
            cursor.execute(id_query, (item_className,))

            recipeIDs = []
            for product in cursor:
                recipeIDs.append(product['recipeID'])

            specifiers = ', '.join(['%s'] * len(recipeIDs))
            recipes_query = f"""
                SELECT * FROM Recipes WHERE id IN ({specifiers})
            """
            cursor.execute(recipes_query, recipeIDs)
            return cursor.fetchall()
    except TypeError as e:
        print(f'{e}\n{item_className} is not a string')

def get_nonalt_recipe(item_className: str):
    """Get original recipe of an item using the item's className"""
    nonalt = None
    try:
        for recipe in get_recipes(item_className):
            if get_main_product(recipe['className'])['item'] == item_className and not recipe['alternate']:     # prioritize recipes in which the item passed in is not a byproduct
                return recipe
            elif not recipe['alternate'] and nonalt is None:
                nonalt = recipe
        if nonalt is None:
            print(f'Warning: get_nonalt_recipe returning None (item: {item_className})')
        return nonalt
    except TypeError as e:
        print(f'{e}\n{item_className} is not a string')

def get_recipe(name: str):
    """Get the recipe of an item using the recipe's in-game name"""
    try:
        with db.cursor(dictionary=True) as cursor:
            query = """
                SELECT * FROM Recipes WHERE name=%s
            """
            cursor.execute(query, (name,))
            res = cursor.fetchone()
            if res:
                return res
            else:
                print(f'Warning: get_recipe returning None (name: {name})')
                return None
    except TypeError as e:
        print(f'{e}\n{name} is not a string')

def get_item(item: str):
    """Get item record of an item using its in-game name"""
    try:
        with db.cursor(dictionary=True) as cursor:
            query = """
                SELECT * FROM Items WHERE name=%s
            """
            cursor.execute(query, (item,))
            res = cursor.fetchone()
            if res:
                return res
            else:
                print(f'Warning: get_item returning None (item: {item})')
                return None
    except TypeError as e:
        print(f'{e}\n{item} is not a string')

def get_main_product(recipe_name: str):
    """Get the main product of a recipe using its className"""      # main product is always the first one
    try:
        with db.cursor(dictionary=True) as cursor:
            query = """
                SELECT * FROM Products WHERE recipeID=
                    (SELECT id FROM Recipes WHERE className=%s)
            """
            cursor.execute(query, (recipe_name,))
            res = cursor.fetchall()
            if res:
                return res[0]
            else:
                print(f'Warning: get_product returning None (recipe name: {recipe_name})')
                return None
    except TypeError as e:
        print(f'{e}\n{recipe_name} is not a string')

def get_building(className: str):
    """Get the record for a building using its className"""
    try:
        with db.cursor(dictionary=True) as cursor:
            query = """
                SELECT * FROM Buildings WHERE className=%s
            """
            cursor.execute(query, (className,))
            res = cursor.fetchone()
            if res:
                return res
            else:
                print(f'Warning: get_building returning None (className: {className})')
                return None
    except TypeError as e:
        print(f'{e}\n{className} is not a string')

def get_all_items():
    """Get all items in database"""
    with db.cursor(dictionary=True) as cursor:
        query = """
            SELECT * FROM Items
        """
        cursor.execute(query)
        res = cursor.fetchall()
        if res:
            return res
        else:
            print(f'Warning: get_all_items returning None')
            return None

def get_all_recipes():
    """Get all recipes in database"""
    with db.cursor(dictionary=True) as cursor:
        query = """
            SELECT * FROM Recipes
        """
        cursor.execute(query)
        res = cursor.fetchall()
        if res:
            return res
        else:
            print(f'Warning: get_all_recipes returning None')
            return None

def get_search_items(input: str):
    """Returns items with names containing the search input"""
    with db.cursor(dictionary=True) as cursor:
        query = """
            SELECT name FROM Items WHERE name LIKE %s
        """
        cursor.execute(query, (f'%{input}%',))
        res = cursor.fetchall()
        names = []
        for r in res:
            names.append(r['name'])
        return names

def get_search_recipes(item: str):
    """Returns recipes with products containing the searched item"""
    with db.cursor(dictionary=True) as cursor:
        recipeIDs = []
        f_query = """
            SELECT recipeID FROM Products WHERE item =
                (SELECT className FROM Items WHERE name = %s)
        """
        cursor.execute(f_query, (item,))
        f_query_res = cursor.fetchall()
        for r in f_query_res:
            recipeIDs.append(r['recipeID'])

        if recipeIDs:
            specifiers = ','.join(['%s'] * len(recipeIDs))
            s_query = f"""
                SELECT name FROM Recipes WHERE id IN ({specifiers})
            """
            cursor.execute(s_query, recipeIDs)
            s_query_res = cursor.fetchall()
            names = []
            recipes = []
            for r in s_query_res:
                names.append(r['name'])

            for recipe_name in names:
                ingredients = []
                for ingredient in get_ingredients(recipe_name):
                    ingredients.append(f'{ingredient['amount']}x {to_name(ingredient['item'])}')

                products = []
                for product in get_products(recipe_name):
                    products.append(f'{product['amount']}x {to_name(product['item'])}')

                recipes.append({
                    'name': recipe_name,
                    'ingredients': ', '.join(ingredients),
                    'products': ', '.join(products)
                })

            return recipes
        else:
            return []

def search_raw_resources(input: str):
    """Returns raw resources with names containing the search input"""
    with db.cursor(dictionary=True) as cursor:
        query = """
            SELECT name FROM Items WHERE isRawResource = 1 AND name LIKE %s
        """
        cursor.execute(query, (f'%{input}%',))
        res = cursor.fetchall()
        names = []
        for r in res:
            names.append(r['name'])
        return names

def to_className(item: str):
    """Returns the className of an item using its in-game name"""
    try:
        with db.cursor(dictionary=True) as cursor:
            query = """
                SELECT className FROM Items WHERE name=%s
            """
            cursor.execute(query, (item,))
            res = cursor.fetchone()
            if res:
                return res['className']
            else:
                print(f'Warning: to_className returning None (item: {item})')
                return None
    except TypeError as e:
        print(f'{e}\n{item} is not a string')

def to_name(className: str):
    """Returns the in-game name of an item using its className"""
    try:
        with db.cursor(dictionary=True) as cursor:
            query = """
                SELECT name FROM Items WHERE className=%s
            """
            cursor.execute(query, (className,))
            res = cursor.fetchone()
            if res:
                return res['name']
            else:
                print(f'Warning: to_name returning None (className: {className})')
                return None
    except TypeError as e:
        print(f'{e}\n{className} is not a string')

def recipe_name_to_className(recipe: str):
    """Returns the className of a recipe using its recipe name"""
    try:
        with db.cursor(dictionary=True) as cursor:
            query = """
                SELECT className FROM Recipes WHERE name=%s
            """
            cursor.execute(query, (recipe,))
            res = cursor.fetchone()
            if res:
                return res['className']
            else:
                print(f'Warning: recipe_name_to_className returning None (name: {recipe})')
                return None
    except TypeError as e:
        print(f'{e}\n{recipe} is not a string')

def recipe_className_to_name(className: str):
    """Returns the name of a recipe using its className"""
    try:
        with db.cursor(dictionary=True) as cursor:
            query = """
                SELECT name FROM Recipes WHERE className=%s
            """
            cursor.execute(query, (className,))
            res = cursor.fetchone()
            if res:
                return res['name']
            else:
                print(f'Warning: recipe_className_to_name returning None (className: {className})')
                return None
    except TypeError as e:
        print(f'{e}\n{className} is not a string')

def building_className_to_name(className: str):
    """Returns the name of a building using its className"""
    try:
        with db.cursor(dictionary=True) as cursor:
            query = """
                SELECT name FROM Buildings WHERE className=%s
            """
            cursor.execute(query, (className,))
            res = cursor.fetchone()
            if res:
                return res['name']
            else:
                print(f'Warning: building_className_to_name returning None (className: {className})')
                return None
    except TypeError as e:
        print(f'{e}\n{className} is not a string')