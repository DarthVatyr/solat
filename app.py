from flask import Flask, render_template, redirect, url_for, request, flash, session, g
from functools import wraps
import os
import json
import sqlite3
import pandas as pd
import numpy as np

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY')

app.database = "items.db"

# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

# Route for handling the welcome page logic
@app.route('/')
def welcome():
    # Render a template
    return render_template('welcome.html') 

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    # Check user credentials and redirect to home page if valid
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
          error = 'Invalid Credentials. Please try again.'
        else:
          session['logged_in'] = True
          flash('You were logged in')
          return redirect(url_for('home'))
    return render_template('login.html', error=error)

# Route for handling the logout page logic
@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('welcome'))

# Route for handling the home page logic
@app.route('/home')
@login_required
def home():
  #g.db = connect_db()
  #cursor = g.db.execute('SELECT * FROM posts')
  #posts = [dict(title=row[0],description=row[1]) for row in cursor.fetchall()]
  #g.db.close()
  return render_template('home.html')

# Route for handling the trade page logic
@app.route('/trade')
@login_required
def trade():
    return render_template('trade.html')

# Route for handling the items page logic
@app.route('/items')
@login_required
def items():
  g.db = connect_db()
  cursor = g.db.execute('SELECT * FROM items')
  items = [dict(ID=row[0], Category=row[1], SubCategory=row[2], Name=row[3], Purchasable=row[4], Locations=row[5], Cost=row[6], Capacity=row[7], Volume=row[8], TempLo=row[9], TempHi=row[10], ArmorClass=row[11], Size=row[12], Scope=row[13], Barrel=row[14], Underbarrel=row[15]) for row in cursor.fetchall()]
  g.db.close()
  table = pd.DataFrame(items, columns=["ID", "Category", "SubCategory", "Name", "Purchaseable", "Locations" ,"Cost", "Capacity", "Volume", "TempLo", "TempHi", "ArmorClass","Size", "Scope", "Barrel", "Underbarrel"])
  return render_template('items.html', tables=[table.to_html(classes='data', header='true')])

# Route for handling the calculators page logic
@app.route('/calculators')
@login_required
def calculators():
    return render_template('calculators.html')

# Route for handling the locations page logic
@app.route('/locations')
@login_required
def locations():
    return render_template('locations.html')

def connect_db():
  return sqlite3.connect(app.database)

# Start the server with the 'run()' method
if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)