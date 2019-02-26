from gurobipy import *

#months = [ "sept", "oct", "nov", "des", "jan", "fab"]
months = []
species = []
monthToPlant = {"01":8,"02":9,"03":10,"04":11,"05":12,"06":1,"07":2,"08":3,"09":4,"10":5,"11":6,"12":7}

model = Model("plotify")
myTuple=[]
sumOrg = 0
sumNotOrg = 0
sumOfMonths = {}
sumOfSpecies = {}
listVarsPlots={}

def solve(plots,orders):
    result=[]

    sumAndSetMonths(orders)
    sumAndSetSpecies(orders)
    global months,species
    for plot in plots:
        name=plot['_id']
        x = model.addVars(months,species,  vtype=GRB.BINARY,  name=name)
        listVarsPlots[name]=x
    model.update()
    sumOrganic(orders)
    organicCstr(plots)
    monthCstr(plots)
    plotCstr()
    speciesCstr(plots)
    CstrByOrder(plots,orders)
    model.optimize()
    for v in model.getVars():
        if(v.x == 1.0):
            name = v.varName.split('[')
            speciesAndMonth=name[1].split(',')
            month=speciesAndMonth[0]
            spe=speciesAndMonth[1][:-1]
            for plot in plots:
                if(plot['_id'] == name[0]):
                    plot['month']=month
                    plot['species']=spe
                    result.append(plot)
                    break
            print(name, v.x)
    return result


def sumOrganic(orders):
    global sumNotOrg,sumOrg
    for order in orders:
        if(order['organic']):
            sumOrg += order['amount']
        else:
            sumNotOrg += order['amount']

def sumAndSetMonths(orders):
    global sumOfMonths, months
    for order in orders:
        month = order['date'].split("-")[1]
        month = monthToPlant[month]
        order['date']=month
        if month not in months:
            months.append(month)
        if month not in sumOfMonths:
            sumOfMonths[month] = order['amount']
        else:
            sumOfMonths[month] += order['amount']

def sumAndSetSpecies(orders):
    global sumOfSpecies, species
    for order in orders:
        variety = order['type']
        if variety not in species:
            species.append(variety)
        if variety not in sumOfSpecies:
            sumOfSpecies[variety] = order['amount']
        else:
            sumOfSpecies[variety] += order['amount']

def organicCstr(plots):
    constr = 0
    for plot in plots:
        name = plot['_id']
        if (plot['אורגני'] == 'אורגני'):
            for (mon, spe), value in listVarsPlots[name].items():
                constr += plot['דונם לגידול שלחין'] * value
    model.addConstr(constr >= sumOrg)
    model.addConstr(constr <= sumOrg + 50)
    constr = 0
    for plot in plots:
        name = plot['_id']
        if (plot['אורגני'] == 'רגיל'):
            for (mon, spe), value in listVarsPlots[name].items():
                constr += plot['דונם לגידול שלחין'] * value
    model.addConstr(constr >= sumNotOrg)
    model.addConstr(constr <= sumNotOrg + 50)

def plotCstr():
    for vars in listVarsPlots.values():
        constr = 0
        for (mon, spe), value in vars.items():
            constr += value
        #x1+x2+x3...<=1
        model.addConstr(constr <= 1)

def monthCstr(plots):
    dictCstr={}
    for month in months:
        dictCstr[month] = 0
    for plot in plots:
        name = plot['_id']
        for (mon, spe), value in listVarsPlots[name].items():
            dictCstr[mon] += plot['דונם לגידול שלחין'] * value
    for key,value in dictCstr.items():
        model.addConstr(value >= sumOfMonths[key])
        model.addConstr(value <= sumOfMonths[key] + 50)

def speciesCstr(plots):
    dictCstr={}
    for variety in species:
        dictCstr[variety] = 0
    for plot in plots:
        name = plot['_id']
        for (mon, spe), value in listVarsPlots[name].items():
            dictCstr[spe] += plot['דונם לגידול שלחין'] * value
    for key,value in dictCstr.items():
        model.addConstr(value >= sumOfSpecies[key])
        model.addConstr(value <= sumOfSpecies[key] + 50)

def CstrByOrder(plots,orders):
    dictCstr={}
    i=0
    ctrAutumn=0
    ctrSpring=0
    for order in orders:
        order['id']=i
        dictCstr[i] = 0
        i+=1
    for plot in plots:
        name = plot['_id']
        for order in orders:
            if order['organic'] is True:
                if (plot['אורגני'] == 'אורגני'):
                    value=listVarsPlots[name][(order['date'],order['type'])]
                    dictCstr[order['id']]+= plot['דונם לגידול שלחין'] * value
            elif (plot['אורגני'] == 'רגיל'):
                    value=listVarsPlots[name][(order['date'],order['type'])]
                    dictCstr[order['id']]+= plot['דונם לגידול שלחין'] * value
            # if (plot['מקור מים'] == 'מאגר רהט'):
            #     value = listVarsPlots[name][(order['date'], order['type'])]
            #     if order['stav'] is True:
            #         ctrAutumn += plot['דונם לגידול שלחין'] * value
            #     else:
            #         ctrSpring += plot['דונם לגידול שלחין'] * value

    for key,value in dictCstr.items():
        model.addConstr(value >= orders[key]['amount'])
        model.addConstr(value <= orders[key]['amount'] + 50)
    # model.addConstr(ctrAutumn <= 1500)
    # model.addConstr(ctrSpring <= 900)

# def RahatReservoirCstr(plots):
#     ctrAutumn=0
#     ctrSpring=0
#     for plot in plots:
#         name = plot['_id']
#         if (plot['אורגני'] == 'אורגני'):
#             for (mon, spe), value in listVarsPlots[name].items():
#                 constr += plot['דונם לגידול שלחין'] * value
#     for key,value in dictCstr.items():
#         model.addConstr(value >= sumOfSpecies[key])
#         model.addConstr(value <= sumOfSpecies[key] + 50)