from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt, check_password_hash

app = Flask(__name__)
bcrypt = Bcrypt(app)

# set up the configurations
app.config['SECRET_KEY'] = '91f6d6f8e8d9c5f91efb94922894b60a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diawiki.db' # this set up the path to our database
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 60) # keep the session on for 60 min
db = SQLAlchemy(app)


@app.route('/') # the function will be executed if the web route has '/' or '/home' as extensions
@app.route('/home')
def home():
    return render_template('home.html')


# the following are tabs for the "Type"
@app.route('/types-of-diabetes')
def home():
    return render_template('type.html')

@app.route('/type-1')
def home():
    return render_template('type1.html')

@app.route('/type-2')
def home():
    return render_template('type2.html')

@app.route('/type-generational')
def home():
    return render_template('typeG.html')


# the following are tabs for the "Treatment" 
@app.route('/treatment')
def home():
    return render_template('treatment.html')

@app.route('/treatment-type1')
def home():
    return render_template('treatment1.html')

@app.route('/treatment-type2')
def home():
    return render_template('treatment2.html')

@app.route('/treatment-generational')
def home():
    return render_template('treatmentG.html')


# the following are tabs for other pages
@app.route('/prevention')
def home():
    return render_template('prevention.html')

@app.route('/forum')
def home():
    return render_template('forum.html')

@app.route('/profile')
def home():
    return render_template('profile.html')

@app.route('/statistic')
def home():
    return render_template('statistic.html')

@app.route('/source')
def home():
    return render_template('source.html')