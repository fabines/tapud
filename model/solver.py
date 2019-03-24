from gurobipy import *

months = []
species = []
stav = ['autumn', 'spring']
monthToPlant = {"01": 8, "02": 9, "03": 10, "04": 11, "05": 12, "06": 1, "07": 2, "08": 3, "09": 4,
                "10": 5, "11": 6, "12": 7}


model = Model("plotify")
myTuple = []
sumOrg = 0
sumNotOrg = 0
sumSpring = 0
sumAutumn = 0
priorityDict = {5: "sort", 4: "doreret", 3: "garav", 2: "frost", 1: "rahatSpring",0: "rahatAutumn"}
sumOfMonths = {}
sumOfSpecies = {}
listVarsPlots = {}
BinaryVarsPlots = {}
dictMechanicalSensitivity = {}
dictSkinColor = {}


def reset():
    global model, myTuple, sumOrg, sumNotOrg, sumOfMonths, sumOfSpecies, listVarsPlots, months, species, dictMechanicalSensitivity, dictSkinColor, sumSpring, sumAutumn, BinaryVarsPlots
    model.discardConcurrentEnvs()
    model.reset(0)
    model.resetParams()
    model = Model("plotify")
    myTuple = []
    sumOrg = 0
    sumNotOrg = 0
    sumSpring = 0
    sumAutumn = 0
    sumOfMonths = {}
    sumOfSpecies = {}
    listVarsPlots = {}
    BinaryVarsPlots = {}
    months = []
    species = []
    dictMechanicalSensitivity = {}
    dictSkinColor = {}
    model.update()


def solve(plots, orders, variety):
    global model, months, species
    reset()
    result = []
    orders = sumAndSetMonths(orders)
    sumAndSetSpecies(orders)
    orders = combineOrder(orders)
    isSensitive(variety)
    skinColor(variety)
    for plot in plots:
        name = plot['_id']
        x = model.addVars(months, species, stav, vtype=GRB.INTEGER,  name=name)
        y = model.addVars(2, vtype=GRB.BINARY, name=name)
        listVarsPlots[name] = x
        BinaryVarsPlots[name] = y
    model.update()
    sumOrganic(orders)
    sumSeason(orders)
    allocatePlotCstr(plots)
    organicCstr(plots)
    monthCstr(plots)
    #plotCstr()
    speciesCstr(plots)
    CstrByOrder(plots, orders)
    CstrSort(plots, orders)
    frostCstr(plots)
    doreretCstr(plots)
    garavCstr(plots)
    model.optimize()
    solveAgain()
    result=getResult(plots,result)
    model.terminate()
    model.update()
    return result

def solveAgain():
    global model
    ifSolution = None
    status = model.status
    if status == GRB.UNBOUNDED:
        print('The model cannot be solved because it is unbounded')
        ifSolution = False
    elif status == GRB.OPTIMAL:
        print('The optimal objective is %g' % model.objVal)
        ifSolution = True
    elif status == GRB.INF_OR_UNBD and status == GRB.INFEASIBLE:
        print('Optimization was stopped with status %d' % status)
        ifSolution = False
    i = len(priorityDict)
    while not ifSolution and i >= 0:
        toRemove = model.getConstrByName(priorityDict[i])
        model.remove(toRemove)
        model.optimize()
        status = model.status
        if status == GRB.UNBOUNDED:
            print('The model cannot be solved because it is unbounded')
            ifSolution = False
        elif status == GRB.OPTIMAL:
            print('The optimal objective is %g' % model.objVal)
            ifSolution = True
        elif status == GRB.INF_OR_UNBD or status == GRB.INFEASIBLE:
            print('Optimization was stopped with status %d' % status)
            ifSolution = False
        i -= 1

def getResult(plots,result):
    for v in model.getVars():
        if v.x > 1.0:
            if '[' not in v.varName:
                continue
            name = v.varName.split('[')
            speciesAndMonth = name[1].split(',')
            month = speciesAndMonth[0]
            spe = speciesAndMonth[1]
            newPlot={}
            for plot in plots:
                if plot['_id'] == name[0]:
                    newPlot['תיאור מיקום מדוייק'] = plot['תיאור מיקום מדוייק']
                    newPlot['שם חלקה מפורט'] = plot['שם חלקה מפורט']
                    newPlot['אורגני'] = plot['אורגני']
                    newPlot['month'] = month
                    newPlot['species'] = spe
                    newPlot['amount'] = v.x
                    if plot['גרב אבקי'] is not None and plot['גרב אבקי'] >= 1 and month != 9:
                        newPlot['אדיגן'] = '60 ליטר/דונם'
                    elif plot['דוררת'] is not None and plot['דוררת'] > 25 and month > 3:
                        newPlot['אדיגן'] = '43 ליטר/דונם'
                    else:
                        newPlot['אדיגן'] = 'לא נדרש חיטוי'
                    result.append(newPlot)
                    break
            print(v.varName, v.x)
    return result

def combineOrder(orders):
    toRemove = []
    for order in orders:
        for order2 in orders:
            if order2['id'] == order['id']:
                continue
            if order2['id'] in toRemove or order['id'] in toRemove:
                continue
            if order['organic'] == order2['organic'] and order['type'] == order2['type'] and order['date'] == \
                    order2['date'] and order['stav'] == order2['stav']:
                order['amount'] += order2['amount']
                toRemove.append(order2['id'])
    orders[:] = [d for d in orders if d.get('id') not in toRemove]
    print(orders)
    return orders


def sumOrganic(orders):
    global sumNotOrg, sumOrg
    for order in orders:
        if order['organic']:
            sumOrg += order['amount']
        else:
            sumNotOrg += order['amount']

def sumSeason(orders):
    global sumSpring, sumAutumn
    for order in orders:
        if order['stav']:
            sumAutumn += order['amount']
        else:
            sumSpring += order['amount']


def sumAndSetMonths(orders):
    global sumOfMonths, months
    for order in orders:
        month = order['date'].split("-")[1]
        month = monthToPlant[month]
        order['date'] = month
        if month not in months:
            months.append(month)
        if month not in sumOfMonths:
            sumOfMonths[month] = order['amount']
        else:
            sumOfMonths[month] += order['amount']
        if order['stav'] is True:
            order['stav'] = 'autumn'
        else:
            order['stav'] = 'spring'
    return orders


def sumAndSetSpecies(orders):
    global sumOfSpecies, species
    for order in orders:
        varietyOrder = order['type']
        if varietyOrder not in species:
            species.append(varietyOrder)
        if varietyOrder not in sumOfSpecies:
            sumOfSpecies[varietyOrder] = order['amount']
        else:
            sumOfSpecies[varietyOrder] += order['amount']

def allocatePlotCstr(plots):
    for plot in plots:
        constr = 0
        name = plot['_id']
        for (mon, spe, season), value in listVarsPlots[name].items():
            constr += value
        min1 = float(plot['דונם לגידול שלחין']-5)
        max1 = float(plot['דונם לגידול שלחין'])
        model.addConstr((BinaryVarsPlots[name][0] == 1) >> (constr == 0))
        #model.addRange(constr, min, plot['דונם לגידול שלחין'])
        model.addConstr((BinaryVarsPlots[name][1] == 1) >> (constr == max1))
        #model.addConstr((listBinaryVarsPlots[name][1] == 1) >> (constr > min))
        model.addConstr(BinaryVarsPlots[name][0] + BinaryVarsPlots[name][1] == 1)


def organicCstr(plots):
    constr = 0
    for plot in plots:
        name = plot['_id']
        if plot['אורגני'] == 'אורגני':
            for (mon, spe, season), value in listVarsPlots[name].items():
                constr += value
    #model.addRange(constr, sumOrg, sumOrg + 5)
    model.addConstr(constr == sumOrg, name='organic')
    #model.addConstr(constr <= sumOrg + 5)
    constr = 0
    for plot in plots:
        name = plot['_id']
        if plot['אורגני'] == 'רגיל':
            for (mon, spe, season), value in listVarsPlots[name].items():
                constr += value
    #model.addRange(constr, sumNotOrg, sumNotOrg+5)
    model.addConstr(constr == sumNotOrg, name='notOrganic')
    #model.addConstr(constr <= sumNotOrg + 5)

# def plotCstr():
#     for vars in listVarsPlots.values():
#         constr = 0
#         for (mon, spe, season), value in vars.items():
#             constr += value
#         # x1+x2+x3...<=1
#         model.addConstr(constr <= 1)


def monthCstr(plots):
    dictCstr = {}
    for month in months:
        dictCstr[month] = 0
    for plot in plots:
        name = plot['_id']
        for (mon, spe, season), value in listVarsPlots[name].items():
            dictCstr[mon] += value
    for key, value in dictCstr.items():
        #model.addRange(value, sumOfMonths[key], sumOfMonths[key]+5)
        model.addConstr(value == sumOfMonths[key])
        #model.addConstr(value <= sumOfMonths[key] + 5)


def speciesCstr(plots):
    dictCstr = {}
    for var in species:
        dictCstr[var] = 0
    for plot in plots:
        name = plot['_id']
        for (mon, spe, season), value in listVarsPlots[name].items():
            if (dictMechanicalSensitivity[spe] == 1 or dictSkinColor[spe] == 'yellow') and plot['איזור גידול'] == 'בית קמה':
                continue
            else:
                dictCstr[spe] += value
    for key, value in dictCstr.items():
        #model.addRange(value, sumOfSpecies[key], sumOfSpecies[key] + 5)
        model.addConstr(value == sumOfSpecies[key])
        #model.addConstr(value <= sumOfSpecies[key] + 5)


def CstrByOrder(plots, orders):
    dictCstr = {}
    i = 0
    for order in orders:
        order['id'] = i
        dictCstr[i] = 0
        i += 1
    for plot in plots:
        name = plot['_id']
        for order in orders:
            if order['organic'] is True:
                if plot['אורגני'] == 'אורגני':
                    value = listVarsPlots[name][(order['date'], order['type'], order['stav'])]
                    dictCstr[order['id']] += value
            elif plot['אורגני'] == 'רגיל':
                value = listVarsPlots[name][(order['date'], order['type'], order['stav'])]
                dictCstr[order['id']] += value

    for key, value in dictCstr.items():
        model.addRange(value, orders[key]['amount'], orders[key]['amount'] + 5)
        #model.addConstr(value == orders[key]['amount'])
        #model.addConstr(value <= orders[key]['amount'] + 5)


def CstrSort(plots, orders):
    dictCstr = {}
    i = 0
    for order in orders:
        order['id'] = i
        dictCstr[i] = 0
        i += 1
    for plot in plots:
        name = plot['_id']
        for order in orders:
            if order['sort'] is False and plot['איזור גידול'] == 'בית קמה':
                continue
            else:
                value = listVarsPlots[name][(order['date'], order['type'], order['stav'])]
                dictCstr[order['id']] += value

    for key, value in dictCstr.items():
        model.addRange(value, orders[key]['amount'], orders[key]['amount'] + 5, name='sort')


def RahatReservoirCstr(plots):
    ctrAutumn = 0
    ctrSpring = 0
    for plot in plots:
        name = plot['_id']
        if plot['מקור מים'] == 'מאגר רהט':
            for (mon, spe, season), value in listVarsPlots[name].items():
                if season == 'autumn':
                    ctrAutumn += value
                else:
                    ctrSpring += value

    model.addConstr(ctrAutumn <= 1500, name='rahatAutumn')
    model.addConstr(ctrSpring <= 900, name='rahatSpring')

def frostCstr(plots):
    constr = 0
    for plot in plots:
        name = plot['_id']
        for (mon, spe, season), value in listVarsPlots[name].items():
            if season == 'autumn' and plot['רגישות לקרה'] == 'רגיש':
                continue
            else:
                constr += value
    #model.addRange(constr, (sumOrg + sumNotOrg), (sumOrg + sumNotOrg) + 5)
    model.addConstr(constr == (sumOrg + sumNotOrg), name='frost')
    #model.addConstr(constr <= (sumOrg + sumNotOrg + 5))

def doreretCstr(plots):
    constr = 0
    for plot in plots:
        name = plot['_id']
        for (mon, spe, season), value in listVarsPlots[name].items():
            if plot['דוררת'] is not None and plot['דוררת'] > 25 and mon > 3:
                continue
            else:
                constr += value
    #model.addRange(constr, (sumOrg + sumNotOrg), (sumOrg + sumNotOrg) + 5)
    model.addConstr(constr == (sumOrg + sumNotOrg), name='doreret')

def garavCstr(plots):
    constr = 0
    for plot in plots:
        name = plot['_id']
        for (mon, spe, season), value in listVarsPlots[name].items():
            if plot['גרב אבקי'] is not None and plot['גרב אבקי'] >= 1 and mon != 9:
                continue
            else:
                constr += value
    #model.addRange(constr, (sumOrg + sumNotOrg), (sumOrg + sumNotOrg) + 5)
    model.addConstr(constr == (sumOrg + sumNotOrg), name='garav')


def isSensitive(variety):
    global dictMechanicalSensitivity
    for var in variety['docs']:
        if var['Variety'] in species:
            if var['Mechanical_damage'] is not None and var['Mechanical_damage'] >= 3:
                dictMechanicalSensitivity[var['Variety']] = 1
            else:
                dictMechanicalSensitivity[var['Variety']] = 0


def skinColor(variety):
    global dictSkinColor
    for var in variety['docs']:
        if var['Variety'] in species:
            if var['Skin_color'] is not None:
                if var['Skin_color'] == 'yellow':
                    dictSkinColor[var['Variety']] = 'yellow'
                else:
                    dictSkinColor[var['Variety']] = 'red'
            else:
                dictSkinColor[var['Variety']] = 'notColor'
