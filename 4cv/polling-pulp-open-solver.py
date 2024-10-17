from pulp import LpMinimize, LpProblem, LpVariable, lpSum

# Define the problem
problem = LpProblem("Store_Visit_Optimization_Two_Weeks", LpMinimize)

# Decision variables for 10 days
x = LpVariable.dicts("Visit", [(i, j) for i in range(4) for j in range(10)], cat='Binary')

# Objective function
problem += lpSum(x[i, j] * sample_data[i]['Distance'] for i in range(4) for j in range(10))

# Constraints
for i, store in enumerate(sample_data):
    if store['Frequency'] == 'EOW':
        problem += lpSum(x[i, j] for j in range(10)) == 1
    elif store['Frequency'] == 'TTW':
        problem += lpSum(x[i, j] for j in range(10)) == 4
    elif store['Frequency'] == 'OAW':
        problem += lpSum(x[i, j] for j in range(10)) == 2
    elif store['Frequency'] == '3TW':
        problem += lpSum(x[i, j] for j in range(10)) == 6

# Volume balance constraints for each day
daily_volume = [lpSum(x[i, j] * sample_data[i]['Demand'] for i in range(4)) for j in range(10)]
average_volume = sum(daily_volume) / 10
for volume in daily_volume:
    problem += volume >= average_volume * 0.9
    problem += volume <= average_volume * 1.1

# Solve the problem
problem.solve()

# Output results
for i in range(4):
    print(f"Store {sample_data[i]['Store']} visits: {[x[i, j].varValue for j in range(10)]}")
