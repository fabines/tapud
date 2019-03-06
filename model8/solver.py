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
sumOfMonths = {}
sumOfSpecies = {}
listVarsPlots = {}
dictMechanicalSensitivity = {}
dictSkinColor = {}


def reset():
    global model, myTuple, sumOrg, sumNotOrg, sumOfMonths, sumOfSpecies, listVarsPlots, months, species, dictMechanicalSensitivity, dictSkinColor, sumSpring, sumAutumn
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
    combineOrder(orders)
    isSensitive(variety)
    skinColor(variety)
    for plot in plots:
        name = plot['_id']
        x = model.addVars(months, species, stav, vtype=GRB.BINARY,  name=name)
        listVarsPlots[name] = x
    model.update()
    sumOrganic(orders)
    sumSeason(orders)
    organicCstr(plots)
    monthCstr(plots)
    plotCstr()
    speciesCstr(plots)
    CstrByOrder(plots, orders)
    frostCstr(plots)
    model.optimize()
    for v in model.getVars():
        if v.x == 1.0:
            name = v.varName.split('[')
            speciesAndMonth = name[1].split(',')
            month = speciesAndMonth[0]
            spe = speciesAndMonth[1]
            for plot in plots:
                if plot['_id'] == name[0]:
                    plot['month'] = month
                    plot['species'] = spe
                    result.append(plot)
                    break
            print(name, v.x)
    model.terminate()
    model.update()
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
        if plot['אורגני'] == 'אורגני':
            for (mon, spe, season), value in listVarsPlots[name].items():
                constr += plot['דונם לגידול שלחין'] * value
    model.addConstr(constr >= sumOrg)
    model.addConstr(constr <= sumOrg + 20)
    constr = 0
    for plot in plots:
        name = plot['_id']
        if plot['אורגני'] == 'רגיל':
            for (mon, spe, season), value in listVarsPlots[name].items():
                constr += plot['דונם לגידול שלחין'] * value
    model.addConstr(constr >= sumNotOrg)
    model.addConstr(constr <= sumNotOrg + 20)

def plotCstr():
    for vars in listVarsPlots.values():
        constr = 0
        for (mon, spe, season), value in vars.items():
            constr += value
        # x1+x2+x3...<=1
        model.addConstr(constr <= 1)


def monthCstr(plots):
    dictCstr = {}
    for month in months:
        dictCstr[month] = 0
    for plot in plots:
        name = plot['_id']
        for (mon, spe, season), value in listVarsPlots[name].items():
            dictCstr[mon] += plot['דונם לגידול שלחין'] * value
    for key, value in dictCstr.items():
        model.addConstr(value >= sumOfMonths[key])
        model.addConstr(value <= sumOfMonths[key] + 20)


def speciesCstr(plots):
    dictCstr = {}
    for variety in species:
        dictCstr[variety] = 0
    for plot in plots:
        name = plot['_id']
        for (mon, spe, season), value in listVarsPlots[name].items():
            if (dictMechanicalSensitivity[spe] == 1 or dictSkinColor[spe] == 'yellow') and plot['איזור גידול'] == 'בית קמה':
                continue
            else:
                dictCstr[spe] += plot['דונם לגידול שלחין'] * value
    for key, value in dictCstr.items():
        model.addConstr(value >= sumOfSpecies[key])
        model.addConstr(value <= sumOfSpecies[key] + 20)


def CstrByOrder(plots, orders):
    dictCstr = {}
    i = 0
    ctrAutumn = 0
    ctrSpring = 0
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
                    dictCstr[order['id']] += plot['דונם לגידול שלחין'] * value
            elif plot['אורגני'] == 'רגיל':
                value = listVarsPlots[name][(order['date'], order['type'], order['stav'])]
                dictCstr[order['id']] += plot['דונם לגידול שלחין'] * value

    for key, value in dictCstr.items():
        model.addConstr(value >= orders[key]['amount'])
        model.addConstr(value <= orders[key]['amount'] + 20)


def RahatReservoirCstr(plots):
    ctrAutumn = 0
    ctrSpring = 0
    for plot in plots:
        name = plot['_id']
        if plot['מקור מים'] == 'מאגר רהט':
            for (mon, spe, season), value in listVarsPlots[name].items():
                if season == 'autumn':
                    ctrAutumn += plot['דונם לגידול שלחין'] * value
                else:
                    ctrSpring += plot['דונם לגידול שלחין'] * value

    model.addConstr(ctrAutumn <= 1500)
    model.addConstr(ctrSpring <= 900)

def frostCstr(plots):
    constr = 0
    for plot in plots:
        name = plot['_id']
        for (mon, spe, season), value in listVarsPlots[name].items():
            if season == 'autumn' and plot['רגישות לקרה'] == 'רגיש':
                continue
            else:
                constr += plot['דונם לגידול שלחין'] * value
    model.addConstr(constr >= (sumOrg + sumNotOrg))
    model.addConstr(constr <= (sumOrg + sumNotOrg + 20))


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
