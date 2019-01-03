from gurobipy import *

try:

    # Create a new model
    m = Model("mip1")
    # Create variables
    f1 = m.addVar(vtype=GRB.BINARY, name="sibir")
    f2 = m.addVar(vtype=GRB.BINARY, name="sibir1")
    f3 = m.addVar(vtype=GRB.BINARY, name="sibir2")

    # Set objective
    # m.setObjective(x + y + 2 * z, GRB.MAXIMIZE)

    # Add constraint: x + 2 y + 3 z <= 4
    m.addConstr(100*f1 + 200 * f2 + 50 * f3 == 150, "c0")

    # Add constraint: x + y >= 1
    # m.addConstr(f1 + f2 >= 1, "c1")

    m.optimize()

    for v in m.getVars():
        print(v.varName, v.x)

    print('Obj:', m.objVal)

except GurobiError:
    print('Error reported')
