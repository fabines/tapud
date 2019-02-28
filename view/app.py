from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, Response, jsonify
from wtforms import Form, StringField, TextAreaField, validators, IntegerField, BooleanField, SelectField
from wtforms.fields.html5 import DateField
import calendar

import sys

sys.path.append('../')
from model.main import *
from model.getFromDB import *
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)
f = first_try()
db = f.connection_to_database()
species = getSpecies(db)
List_input = []
i=0
listOfUsers = [
    {
        'username': 'Admin',
        'password': sha256_crypt.encrypt(str(1234))
    }
]

# todo insert to controller
def createTuppleSpecies(species):
    listTuple = []
    for variety in species['docs']:
        listTuple.append(tuple((variety['Variety'], variety['species'])))
    return listTuple


newSpecies = createTuppleSpecies(species)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


# Single Plot
@app.route('/plot/<string:id>/')
def article(id):
    # Create cursor
    Plot = {
        'id': 1,
        'title': 'Plot One',
        'body': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        'author': 'Brad Traversy',
        'create_date': '04-25-2017'
    }
    return render_template('plot.html', plot=Plot)


# plot Form Class
class PlotForm(Form):
    amount = IntegerField('Amount', [validators.required()])
    # type = StringField('Type', [validators.Length(min=4, max=25)])
    default = [('1', "select species")]
    default.extend(newSpecies)
    type = SelectField('Type', [validators.NoneOf(['1'], message="you must select species")], choices=default)
    date = DateField('Date', format='%Y-%m-%d')
    organic = BooleanField('Organic', [validators.AnyOf([True, False])])
    stav = BooleanField('Automn sowing', [validators.AnyOf([True, False])])


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))

    return wrap


# table

# other column settings -> http://bootstrap-table.wenzhixin.net.cn/documentation/#column-options
columns = [
    {
        "field": "plot_name",  # which is the field's name of data key
        "title": "שם חלקה",  # display as the table header's name
        "sortable": True,
    },
    {
        "field": "month2sow",
        "title": "חודש זריעה",
        "sortable": True,
    },
    {
        "field": "species",
        "title": "זן",
        "sortable": True,
    },
    {
        "field": "type",
        "title": "סוג חלקה",
        "sortable": True,
    }
]
def initTableResult(plots):
    data=[]
    for plot in plots:
        row={}
        row['plot_name']=plot['שם חלקה מפורט']
        row['month2sow']=calendar.month_name[int(plot['month'])]
        row['species']=plot['species']
        row['type']=plot['אורגני']
        data.append(row)
    return data

def index(data):
    return render_template("table.html",
                           data=data,
                           columns=columns,
                           title='חלקות לזריעה')


# order
@app.route('/order', methods=['GET', 'POST'])
@is_logged_in
def order():
    global List_input,i
    form = PlotForm(request.form)
    if request.method == 'POST' and form.validate():
        if request.form['submit_button'] == 'Add':
            order = {}
            order['id']=i
            order['amount'] = form.amount.data
            order['type'] = form.type.data
            order['date'] = form.date.data.strftime('%d-%m-%Y')
            order['organic'] = form.organic.data
            order['stav'] = form.stav.data
            List_input.append(order)
            i+=1
            print(List_input)
            #flash('Order added successfully', 'success')
            return render_template('order.html', form=form, orders=List_input)
            #redirect(url_for('order', orders=List_input))
        elif request.form['submit_button'] == 'Submit':
            order = {}
            order['id'] = i
            order['amount'] = form.amount.data
            order['type'] = form.type.data
            order['date'] = form.date.data.strftime('%d-%m-%Y')
            order['organic'] = form.organic.data
            order['stav'] = form.stav.data
            List_input.append(order)
            i=0
            print(List_input)
            #flash('Order added successfully', 'success')
            Plots = f.getPlots(db, List_input)
            List_input = []
            data= initTableResult(Plots)
            return index(data)
            # return render_template('plots.html', plots=Plots)
    return render_template('order.html', form=form ,orders=List_input)

@app.route('/delete_order/<string:id>', methods=['POST'])
@is_logged_in
def delete_order(id):
    print(id)
    global List_input
    #List_input = [i for i in List_input if not (i['id'] == id)]
    for j in range(len(List_input)):
        if List_input[j]['id'] == int(id):
            del List_input[j]
            break
    #flash('order Deleted', 'success')
    print(List_input)
    return redirect(url_for('order', orders=List_input))

    #return render_template('order.html', orders=List_input)

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
