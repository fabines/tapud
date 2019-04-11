from flask import Flask, render_template, flash, redirect, url_for, session, request
from wtforms import Form, RadioField, validators, IntegerField, BooleanField, SelectField, StringField
from wtforms.fields.html5 import DateField
import calendar
from flask import Markup
from model.main import *
from model.getFromDB import *
from model.solver import *
from passlib.hash import sha256_crypt
from functools import wraps
import sys

sys.path.append('../')

app = Flask(__name__)
f = first_try()
db = f.connection_to_database()
species = getSpecies(db)
List_input = []
list_View = []
i = 0
listOfUsers = [
    {
        'username': 'Admin',
        'password': sha256_crypt.encrypt(str(1234))
    }
]


# todo insert to controller


def createTuppleSpecies(specie):
    listTuple = []
    newlist = sorted(specie['docs'], key=lambda k: k['species'])
    for variety in newlist:
        listTuple.append(tuple((variety['Variety'], variety['species'])))
    return listTuple


newSpecies = createTuppleSpecies(species)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')



# plot Form Class
class orderForm(Form):
    customer = StringField('Customer', [validators.required()])
    amount = IntegerField('Amount', [validators.required()])
    # type = StringField('Type', [validators.Length(min=4, max=25)])
    default = [('1', "select species")]
    default.extend(newSpecies)
    variety = SelectField('Variety', [validators.NoneOf(['1'], message="you must select species")], choices=default)
    date = DateField('Date', format='%Y-%m-%d')
    organic = BooleanField('Organic', [validators.AnyOf([True, False])])


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))

    return wrap


def initTableResult(plots):
    data = []
    for plot in plots:
        row = {}
        if plot['תיאור מיקום מדוייק'] is not None:
            row['plot_name'] = plot['שם חלקה מפורט'] + ' : ' + plot['תיאור מיקום מדוייק']
        else:
            row['plot_name'] = plot['שם חלקה מפורט']
        row['amount'] = plot['amount']
        row['month2sow'] = calendar.month_name[int(plot['month'])]
        row['species'] = plot['species']
        row['type'] = plot['אורגני']
        row['edigan'] = plot['אדיגן']
        data.append(row)
    return data


@app.route('/species', methods=['POST'])
def funcSpecies():
    formSpe = SpeciesForm(request.form)
    if formSpe.validate():
        print('hello')
    return render_template('update.html', speForm=formSpe)


# order
@app.route('/order', methods=['GET', 'POST'])
@is_logged_in
def order():
    global List_input, i, list_View
    form = orderForm(request.form)
    if request.method == 'POST':
        if form.validate() and request.form['submit_button'] == 'Add':
            orderView = {}
            order = {}
            order['id'] = i
            order['customer'] = form.customer.data
            order['amount'] = form.amount.data
            order['type'] = form.variety.data
            order['date'] = form.date.data.strftime('%d-%m-%Y')
            order['organic'] = form.organic.data
            orderView['id'] = i
            orderView['customer'] = form.customer.data
            orderView['amount'] = form.amount.data
            orderView['type'] = form.variety.data
            orderView['date'] = form.date.data.strftime('%d-%m-%Y')
            if form.organic.data is True:
                orderView['organic'] = 'organic'
            else:
                orderView['organic'] = 'regular'
            stav = request.form['stav']
            sort = request.form['sort']
            if stav == 'autumn':
                order['stav'] = True
                orderView['stav'] = 'autumn'
            else:
                order['stav'] = False
                orderView['stav'] = 'spring'
            if sort == 'sort':
                order['sort'] = True
                orderView['sort'] = 'sort'
            else:
                order['sort'] = False
                orderView['sort'] = 'harvest'
            List_input.append(order)
            list_View.append(orderView)
            i += 1
            print(List_input)
            # flash('Order added successfully', 'success')
            return render_template('order.html', form=form, orders=list_View)
            # quest.form['submit_button'] == 'Submit':
        elif request.form['submit_button'] == 'getHistory':
            doc = getHistory(db)
            if doc is None:
                flash('You Don\'t have History', 'danger')
            else:
                List_input = doc['List_input']
                list_View = doc['list_view']
            return render_template('order.html', form=form, orders=list_View)
        elif not List_input:
            flash('You must add orders', 'danger')
        elif request.form['submit_button'] == 'saveToHistory':
            saveToHistory(db, List_input, list_View)
        else:
            i = 0
            print(List_input)
            # flash('Order added successfully', 'success')
            Plots = f.getPlots(db, List_input, species)
            List_input = []
            list_View = []
            data = initTableResult(Plots['result'])
            print(Plots['removed'])
            constr=Plots['removed'][0]
            for i in range(1, len(Plots['removed'])):
                constr+= "<hr><p>"+Plots['removed'][i]+"<p>"
            message = Markup("<h4 class=\"alert-heading\">Removed constraints:</h4><p>"+constr+"</p>")
            flash(message, 'info')
            return render_template('table.html', plots=data)
            # return index(data)
            # return render_template('plots.html', plots=Plots)
    return render_template('order.html', form=form, orders=list_View)


@app.route('/delete_order/<string:id>', methods=['POST'])
@is_logged_in
def delete_order(id):
    print(id)
    global List_input, list_View
    # List_input = [i for i in List_input if not (i['id'] == id)]
    for j in range(len(List_input)):
        if List_input[j]['id'] == int(id):
            del list_View[j]
            del List_input[j]
            break
    # flash('order Deleted', 'success')
    print(List_input)
    return redirect(url_for('order', orders=list_View))

    # return render_template('order.html', orders=List_input)


@app.route('/delete_variety/<string:name>', methods=['POST'])
@is_logged_in
def delete_variety(name):
    print(id)
    # global List_input, list_View
    # # List_input = [i for i in List_input if not (i['id'] == id)]
    # for j in range(len(List_input)):
    #     if List_input[j]['id'] == int(id):
    #         del list_View[j]
    #         del List_input[j]
    #         break
    # # flash('order Deleted', 'success')
    # print(List_input)
    return redirect(url_for('addVariety', varieties = species['docs']))
    # return render_template('order.html', orders=List_input)


@app.route('/updateDB', methods=['GET', 'POST'])
@is_logged_in
def update():
    if request.method == 'POST':
        if request.form['button'] == 'edit':
            doc = db[request.form['ID']]
            doc['מספר חלקה '] = request.form['מספר חלקה']
            doc['מספר חלקה מפורט'] = request.form['מספר חלקה מפורט']
            doc['שם חלקת אם'] = request.form['שם חלקת אם']
            doc['שם חלקה מפורט'] = request.form['שם חלקה מפורט']
            doc['איזור גידול'] = request.form['איזור גידול']
            doc['סוג חלקה'] = request.form['סוג חלקה']
            doc['אורגני'] = request.form['אורגני']
            doc['שטח ברוטו (דונם)'] = request.form['שטח ברוטו']
            doc['מגוף השקייה'] = request.form['מגוף השקייה']
            doc['מקור מים'] = request.form['מקור מים']
            doc['דונם לגידול שלחין'] = float(request.form['דונם לגידול שלחין'])
            doc['תיאור מיקום מדוייק'] = request.form['תיאור מיקום מדוייק']
            if request.form['דוררת'] == 'None':
                doc['דוררת'] = None
            else:
                doc['דוררת'] = float(request.form['דוררת'])
            if request.form['גרב אבקי'] == 'None':
                doc['גרב אבקי'] = None
            else:
                doc['גרב אבקי'] = float(request.form['גרב אבקי'])
            doc['אבנים'] = request.form['אבנים']
            doc['רגישות לקרה'] = request.form['רגישות לקרה']
            doc['חיטוי אדיגן'] = request.form['חיטוי אדיגן']
            doc.save()
        elif request.form['button'] == 'updateYear':
            flash('we did it!!!', 'success')
            doc={}
    plots = getAllPlots(db)
    plots = plots['docs']
    print(plots)
    return render_template('updatePlot.html', plots=plots)


class PreferenceForm(Form):
    doreret = SelectField('Doreret', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7')])
    garav = SelectField('Garav avki', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7')])
    sort = SelectField('Sort', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7')])
    lastCrop = SelectField('Last crop', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7')])
    frost = SelectField('Frost', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7')])
    rahatAutumn = SelectField('Rahat autumn', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'),('7', '7')])
    rahatSpring = SelectField('Rahat spring', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'),('7', '7')])


@app.route('/choosePreference', methods=['GET', 'POST'])
@is_logged_in
def choosePreference():
    form = PreferenceForm(request.form)
    old_priority = getPreferenceList(db)
    if request.method == 'POST':
        priorityDict = {}
        for key,value in form.data.items():
            if int(value) not in priorityDict:
                priorityDict[int(value)] = key
            else:
                flash('Please rank with different preference','danger')
                return render_template('choosePreference.html', form=form, preferences=old_priority)
        savePreferenceList(db, priorityDict)
        old_priority = priorityDict
        flash('Preference saved successfully!', 'success')
    return render_template('choosePreference.html', form=form, preferences=old_priority)


class SpeciesForm(Form):
    HebrewName = StringField('Name in Hebrew', [validators.required(), validators.length(max=20)])
    EnglishName = StringField('Name in English', [validators.required(), validators.length(max=20)])
    skinColor = SelectField('skinColor', choices=[('red', 'אדום'), ('yellow', 'צהוב')])
    Mechanical_damage = IntegerField('Mechanical damage')
    Powdery_scab = IntegerField('Powdery scab')


@app.route('/addVariety', methods=['GET', 'POST'])
@is_logged_in
def addVariety():
    global species
    form = SpeciesForm(request.form)
    if request.method == 'POST':
        newRow = {}
        newRow['_id'] = form.EnglishName.data
        newRow['species'] = form.HebrewName.data
        newRow['Variety'] = form.EnglishName.data
        newRow['Skin_color'] = form.skinColor.data
        newRow['Mechanical_damage'] = form.Mechanical_damage.data
        newRow['Powdery_scab'] = form.Powdery_scab.data
        newRow['type'] = 'species'
        print(newRow)
        try:
            # db.create_document(newRow)
            species = getSpecies(db)
            flash('Variety added successfully', 'success')

        except Exception as e:
            print(type(e))
            print(e.args)
            print(e)
            flash('Somthing went wrong, please try again later', 'danger')

        species = getSpecies(db)
    return render_template('addVariety.html', form=form, varieties=species['docs'])


# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        user = list(filter(lambda person: person['username'] == username, listOfUsers))
        print(user)
        if user:
            password = user[0]['password']
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('order'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')


@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
