import pulp

# 1. Initialize problem
prob = pulp.LpProblem('Maximize_ReinforcedPlate', pulp.LpMaximize)

# 2. Define decision variables
x = pulp.LpVariable('IronPlate', lowBound=0, cat='Continuous')
y = pulp.LpVariable('IronScrew', lowBound=0, cat='Continuous')
z = pulp.LpVariable('ReinforcedPlate', lowBound=0, cat='Continuous')

# 3. Define objective function (Maximize number of reinforced plates produced)
prob += z, 'Total_ReinforcedPlate_Production'

# 4. Define constraints
# Reinforced Plates: 6 plates + 12 screws = 1 reinforced plate
prob += x - 6 * z == 0, 'IronPlate_Requirement'
prob += y - 12 * z == 0, 'Screws_Requirement'

# Iron Plates: 3 ingots make 2 plates => per unit = 1.5 ingots make 1 plate (3/2)
# Cast Screws: 5 ingots make 20 screws => per unit = 0.25 ingots make 1 screw (5/20)
prob += 1.5 * x + 0.25 * y <= 120, 'Available_IronIngots'

# Relationship constraint: For every iron plate, there must be 2 screws (2x = y)
prob += 2 * x - y == 0, 'Ratio_Constraint'

solver = pulp.PULP_CBC_CMD(msg=False)
status = prob.solve(solver)

print(f'Status: {pulp.LpStatus[status]}')
print(f'Optimal number of {x.name}: {x.varValue}')
print(f'Optimal number of {y.name}: {y.varValue}')
print(f'Total reinforced plates produced: {z.varValue}')
print(f'Number of constructors needed for {x.name}: {x.varValue / 30}')
print(f'{int(x.varValue / 30)} constructors at 100%{f', 1 constructor at {round(x.varValue / 30 % 1 * 10, 4)}%' if x.varValue / 30 % 1 != 0 else ''}')
print(f'Number of constructors needed for {y.name}: {y.varValue / 50}')
print(f'{int(y.varValue / 50)} constructors at 100%{f', 1 constructor at {round(y.varValue / 50 % 1 * 100, 4)}%' if y.varValue / 50 % 1 != 0 else ''}')
print(f'Number of assemblers needed for {z.name}: {z.varValue / 5}')
