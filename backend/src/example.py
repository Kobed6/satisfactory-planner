import pulp

# 1. Initialize problem
prob = pulp.LpProblem('Maximize_ReinforcedPlate', pulp.LpMaximize)

# 2. Define decision variables
recipe_reinforced_plates = prob.add_variable('ReinforcedPlate', lowBound=0, cat='Continuous')
recipe_iron_plates = prob.add_variable('IronPlate', lowBound=0, cat='Continuous')
recipe_cast_screws = prob.add_variable('CastScrews', lowBound=0, cat='Continuous')
recipe_iron_ingots = prob.add_variable('IronIngot', lowBound=0, cat='Continuous')

# 3. Define objective function (Maximize number of reinforced plates produced)
prob += recipe_reinforced_plates, 'Total_RecipeRuns_ReinforcedIronPlate'

# 4. Define constraints
# Reinforced Plates: 6 plates + 12 screws = 1 reinforced plate
all_products = {
    'Reinforced Iron Plate': [(1, recipe_reinforced_plates)],
    'Iron Plate': [(2, recipe_iron_plates)],
    'Screws': [(20, recipe_cast_screws)],
    'Iron Ingot': [(1, recipe_iron_ingots)]
}
all_ingredients = {
    'Iron Plate': [(6, recipe_reinforced_plates)],
    'Screws': [(12, recipe_reinforced_plates)],
    'Iron Ingot': [(3, recipe_iron_plates), (5, recipe_cast_screws)],
    'Iron Ore': [(1, recipe_iron_ingots)]
}

# Iron Plates: 6 consumed by reinforced iron plates recipe, 3 produced by iron plates recipe
iron_plates_consumed = all_ingredients['Iron Plate'][0][0] * all_ingredients['Iron Plate'][0][1]
iron_plates_produced = all_products['Iron Plate'][0][0] * all_products['Iron Plate'][0][1]
prob += iron_plates_consumed <= iron_plates_produced

# Screws: 12 consumed by reinforced iron plates, 20 produced by cast screws recipe
screws_consumed = all_ingredients['Screws'][0][0] * all_ingredients['Screws'][0][1]
screws_produced = all_products['Screws'][0][0] * all_products['Screws'][0][1]
prob += screws_consumed <= screws_produced

# Iron Ingots: 3 consumed by iron plates and 5 by cast screws, 1 produced by iron ingot recipe
iron_ingots_consumed = pulp.lpSum(amount * var for amount, var in all_ingredients['Iron Ingot'])
iron_ingots_produced = all_products['Iron Ingot'][0][0] * all_products['Iron Ingot'][0][1]
prob += iron_ingots_consumed <= iron_ingots_produced

# Iron Ore: 1 consumed by iron ingots, 120 produced by miner mk1 on pure node
iron_ores_consumed = pulp.lpSum(amount * var for amount, var in all_ingredients['Iron Ore'])
prob += iron_ores_consumed <= 120, 'Iron_Ore'

solver = pulp.COIN_CMD(msg=False)
status = prob.solve(solver)

final_reinforced_plates_production = recipe_reinforced_plates.varValue * 1
final_iron_plates_production = recipe_iron_plates.varValue * 2
final_cast_screws_production = recipe_cast_screws.varValue * 20
final_iron_ingots_production = recipe_iron_ingots.varValue * 1
print(f'Status: {pulp.LpStatus[status]}')
print(f'{recipe_reinforced_plates.name} times run: {recipe_reinforced_plates.varValue} (amount produced: {final_reinforced_plates_production})')
print(f'{recipe_iron_plates.name} times run: {recipe_iron_plates.varValue} (amount produced: {final_iron_plates_production})')
print(f'{recipe_cast_screws.name} times run: {recipe_cast_screws.varValue} (amount produced: {final_cast_screws_production})')
print(f'{recipe_iron_ingots.name} times run: {recipe_iron_ingots.varValue} (amount produced: {final_iron_ingots_production})')
print(f'Number of assemblers needed for {recipe_reinforced_plates.name}: {final_reinforced_plates_production / 5}')
print(f'Number of constructors needed for {recipe_iron_plates.name}: {final_iron_plates_production / 30}')
print(f'{int(final_iron_plates_production / 30)} constructors at 100%{f', 1 constructor at {round(final_iron_plates_production / 30 % 1 * 10, 4)}%' \
                                                                      if final_iron_plates_production / 30 % 1 != 0 else ''}')
print(f'Number of constructors needed for {recipe_cast_screws.name}: {final_cast_screws_production / 50}')
print(f'{int(final_cast_screws_production / 50)} constructors at 100%{f', 1 constructor at {round(final_cast_screws_production / 50 % 1 * 100, 4)}%' \
                                                                      if final_cast_screws_production / 50 % 1 != 0 else ''}')
