import os
from dotenv import load_dotenv
import numpy as np
import pandas as pd
import mysql.connector

load_dotenv()

db = mysql.connector.connect(
	host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    user=os.getenv('DB_USER'),
    passwd=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
)

cursor = db.cursor()

print('Dropping existing tables...')
cursor.execute('DROP TABLE IF EXISTS Ingredients')
cursor.execute('DROP TABLE IF EXISTS Products')
cursor.execute('DROP TABLE IF EXISTS Recipes')
cursor.execute('DROP TABLE IF EXISTS Buildings')
cursor.execute('DROP TABLE IF EXISTS Items')

print('Creating tables...')
cursor.execute('CREATE TABLE IF NOT EXISTS Recipes (id INT PRIMARY KEY AUTO_INCREMENT, className VARCHAR(50), name VARCHAR(50), \
               unlockedBy VARCHAR(1000), duration INT, producedIn VARCHAR(50), alternate BOOL)')
cursor.execute('CREATE TABLE IF NOT EXISTS Ingredients (id INT PRIMARY KEY AUTO_INCREMENT, recipeID INT, FOREIGN KEY (recipeID) REFERENCES Recipes(id), \
               item VARCHAR(50), amount INT UNSIGNED, amountPerMin FLOAT(3))')
cursor.execute('CREATE TABLE IF NOT EXISTS Products (id INT PRIMARY KEY AUTO_INCREMENT, recipeID INT, FOREIGN KEY (recipeID) REFERENCES Recipes(id), \
               item VARCHAR(50), amount INT UNSIGNED, amountPerMin FLOAT(3))')
cursor.execute('CREATE TABLE IF NOT EXISTS Buildings (id INT PRIMARY KEY AUTO_INCREMENT, className VARCHAR(50), name VARCHAR(50), unlockedBy VARCHAR(50), \
			   powerUsage INT, somersloopSlots INT)')
cursor.execute('CREATE TABLE IF NOT EXISTS Items (id INT PRIMARY KEY AUTO_INCREMENT, className VARCHAR(50), name VARCHAR(50), isRawResource BOOL)')

recipe_insert_query = 'INSERT INTO Recipes (className, name, unlockedBy, duration, producedIn, alternate) VALUES (%s, %s, %s, %s, %s, %s)'
ingredient_insert_query = 'INSERT INTO Ingredients (recipeID, item, amount, amountPerMin) VALUES (%s, %s, %s, %s)'
product_insert_query = 'INSERT INTO Products (recipeID, item, amount, amountPerMin) VALUES (%s, %s, %s, %s)'
building_insert_query = 'INSERT INTO Buildings (className, name, unlockedBy, powerUsage, somersloopSlots) VALUES (%s, %s, %s, %s, %s)'
item_insert_query = 'INSERT INTO Items (className, name, isRawResource) VALUES (%s, %s, %s)'

recipes_s = pd.read_json('data/Template_DocsRecipes.json', typ='series')
recipes_s
recipes_s.sort_values(key=lambda x: x.apply(lambda y: y[0]['name']), inplace=True)

buildings_s = pd.read_json('data/Template_DocsBuildings.json', typ='series')

items_s = pd.read_json('data/Template_DocsItems.json', typ='series')
items_s.sort_values(key=lambda x: x.apply(lambda y: y[0]['name']), inplace=True)

for value in recipes_s:
	data = value[0]
	if data['producedIn'] and data['seasons'] == []:
		item_name = data['name']
		# special case: turbo rifle ammo has two identical recipes with the only difference being their production buildings
		if data['name'] == 'Turbo Rifle Ammo':
			if data['producedIn'][0] == 'Desc_Blender_C':
				item_name = 'Turbo Rifle Ammo (Blender)'
			elif data['producedIn'][0] == 'Desc_ManufacturerMk1_C':
				item_name = 'Turbo Rifle Ammo (Manufacturer)'

		item = (
			data['className'],
			item_name,
			data['unlockedBy'],
			data['duration'],
			data['producedIn'][0],
			data['alternate']
		)
		cursor.execute(recipe_insert_query, item)

		inserted_id = cursor.lastrowid

# add conversion to per min to each ingredient and insert ingredient to SQL database
		for ingredient in data['ingredients']:
			ingredient['amountPerMin'] = ingredient['amount'] * (60 / data['duration'])
			ingredient_tuple = (inserted_id, ingredient['item'], ingredient['amount'], ingredient['amountPerMin'])
			cursor.execute(ingredient_insert_query, ingredient_tuple)

# add conversion to per min to each product and insert product to SQL database
		for product in data['products']:
			product['amountPerMin'] = product['amount'] * (60 / data['duration'])
			product_tuple = (inserted_id, product['item'], product['amount'], product['amountPerMin'])
			cursor.execute(product_insert_query, product_tuple)

for value in buildings_s:
	data = value[0]
	if data['overclockable'] and data['powerGenerated'] == 0:
		building = (
			data['className'],
			data['name'],
			data['unlockedBy'],
			data['powerUsage'],
			data['somersloopSlots']
		)
		cursor.execute(building_insert_query, building)

raw_resources = {'Desc_OreBauxite_C', 'Desc_OreGold_C', 'Desc_Coal_C', 'Desc_Cement_C', 'Desc_OreCopper_C', 'Desc_OreIron_C', 'Desc_Stone_C', 'Desc_RawQuartz_C', \
				 	'Desc_SAM_C', 'Desc_Sulfur_C', 'Desc_OreUranium_C', 'Desc_Shroom_C', 'Desc_Nut_C', 'Desc_GenericBiomass_C', 'Desc_Crystal_C', 'Desc_LiquidOil_C', \
						'Desc_HatcherParts_C', 'Desc_HogParts_C', 'Desc_Leaves_C', 'Desc_NitrogenGas_C', 'Desc_WAT2_C', 'Desc_Mycelia_C', 'Desc_Berry_C', \
							'Desc_Crystal_mk3_C', 'Desc_WAT1_C', 'Desc_SpitterParts_C', 'Desc_StingerParts_C', 'Desc_Water_C', 'Desc_Wood_C', 'Desc_Crystal_mk2_C'}
for value in items_s:
	is_raw_resource = 0
	data = value[0]
	if data['className'] in raw_resources:
		is_raw_resource = 1
	item = (data['className'], data['name'], is_raw_resource)
	cursor.execute(item_insert_query, item)

db.commit()
cursor.close()
db.close()