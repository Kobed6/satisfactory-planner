import pulp

# 1. Initialize problem
prob = pulp.LpProblem('Maximize_ReinforcedPlate', pulp.LpMaximize)

# 2. Define decision variables
iron_plates = pulp.LpVariable('IronPlate', lowBound=0, cat='Continuous')
screws = pulp.LpVariable('IronScrew', lowBound=0, cat='Continuous')
reinforced_plates = pulp.LpVariable('ReinforcedPlate', lowBound=0, cat='Continuous')
iron_ingots = pulp.LpVariable('IronIngot', lowBound=0, cat='Continuous')

# 3. Define objective function (Maximize number of reinforced plates produced)
prob += reinforced_plates, 'Total_ReinforcedPlate_Production'

# 4. Define constraints
# Reinforced Plates: 6 plates + 12 screws = 1 reinforced plate
prob += pulp.lpSum(6 * reinforced_plates) <= iron_plates, 'IronPlate_Requirement'
prob += 12 * reinforced_plates <= screws, 'Screws_Requirement'

# Iron Plates: 3 ingots make 2 plates => per unit = 1.5 ingots make 1 plate (3/2)
# Cast Screws: 5 ingots make 20 screws => per unit = 0.25 ingots make 1 screw (5/20)
var_constraints = {iron_ingots: [1.5 * iron_plates, 0.25 * screws]}
prob += pulp.lpSum(var_constraints[iron_ingots]) <= iron_ingots, 'Available_IronIngots'

prob += iron_ingots <= 120, 'Iron_Ore'

# Relationship constraint: For every iron plate, there must be 2 screws (2x = y)
prob += 2 * iron_plates - screws == 0, 'Ratio_Constraint'

solver = pulp.PULP_CBC_CMD(msg=False)
status = prob.solve(solver)

# for v in prob.variables():
#     print(v, pulp.value(v))
print(f'Status: {pulp.LpStatus[status]}')
print(f'Optimal number of {iron_plates.name}: {iron_plates.varValue}')
print(f'Optimal number of {screws.name}: {screws.varValue}')
print(f'Total reinforced plates produced: {reinforced_plates.varValue}')
print(f'Number of constructors needed for {iron_plates.name}: {iron_plates.varValue / 30}')
print(f'{int(iron_plates.varValue / 30)} constructors at 100%{f', 1 constructor at {round(iron_plates.varValue / 30 % 1 * 10, 4)}%' if iron_plates.varValue / 30 % 1 != 0 else ''}')
print(f'Number of constructors needed for {screws.name}: {screws.varValue / 50}')
print(f'{int(screws.varValue / 50)} constructors at 100%{f', 1 constructor at {round(screws.varValue / 50 % 1 * 100, 4)}%' if screws.varValue / 50 % 1 != 0 else ''}')
print(f'Number of assemblers needed for {reinforced_plates.name}: {reinforced_plates.varValue / 5}')
