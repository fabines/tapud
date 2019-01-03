from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, validators, IntegerField
import sys
sys.path.append('../')
from model.main import *
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)
f = first_try()
db = f.connection_to_database()
List_input = []
listOfUsers=[
    {
        'username': 'Admin',
        'password': sha256_crypt.encrypt(str(1234))
    }
]

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

#Single Plot
@app.route('/plot/<string:id>/')
def article(id):
    # Create cursor
    Plot={
            'id': 1,
            'title':'Plot One',
            'body':'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
            'author':'Brad Traversy',
            'create_date':'04-25-2017'
        }
    return render_template('plot.html', plot=Plot)

# plot Form Class
class PlotForm(Form):
    amount =  IntegerField('Amount', [validators.required()])
    type = StringField('Type', [validators.Length(min=4, max=25)])
    date = StringField('Date', [validators.Length(min=6, max=50)])
    organic = StringField('Organic', [validators.DataRequired(),
    ])

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# order
@app.route('/order', methods=['GET', 'POST'])
@is_logged_in
def order():
    global List_input
    form = PlotForm(request.form)
    if request.method == 'POST' and form.validate():
        if request.form['submit_button']=='add':
            order={}
            order['amount'] = form.amount.data
            order['type'] = form.type.data
            order['date'] = form.date.data
            order['organic'] = form.organic.data
            List_input.append(order)
            print(List_input)
            flash('Order added successfully', 'success')
            return redirect(url_for('order'))
        elif request.form['submit_button']=='submit':
            order = {}
            order['amount'] = form.amount.data
            order['type'] = form.type.data
            order['date'] = form.date.data
            order['organic'] = form.organic.data
            List_input.append(order)
            print(List_input)
            flash('Order added successfully', 'success')
            Plots = f.getPlots(db, List_input)
            List_input=[]
            return render_template('plots.html', plots=Plots)
    return render_template('order.html', form=form)

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        user = list(filter(lambda person: person['username'] == username, listOfUsers))
        print (user)
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
    app.secret_key='secret123'
    app.run(debug=True)
