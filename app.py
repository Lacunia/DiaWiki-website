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
bcrypt = Bcrypt(app)

# databases
class Person(db.Model):
    __tablename__ = 'Person'
    username = db.Column(db.String(20), primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable = False)

    def __repr__(self):
        return f"Person('{self.username}', '{self.email}')"

with app.app_context(): # create any database that are new
    db.create_all()


@app.route('/') # the function will be executed if the web route has '/' or '/home' as extensions
@app.route('/home')
def home():
    return render_template('home.html')


# the following are tabs for the "Type"
@app.route('/type')
def type():
    return render_template('type.html')

@app.route('/type1')
def type1():
    return render_template('type1.html')

@app.route('/type2')
def type2():
    return render_template('type2.html')

@app.route('/typeGl')
def typeG():
    return render_template('typeG.html')


# the following are tabs for the "Treatment" 
@app.route('/treatment')
def treatment():
    return render_template('treatment.html')

@app.route('/treatment1')
def treatment1():
    return render_template('treatment1.html')

@app.route('/treatment2')
def treatment2():
    return render_template('treatment2.html')

@app.route('/treatmentG')
def treatmentG():
    return render_template('treatmentG.html')


# the following are tabs for other pages
@app.route('/prevention')
def prevention():
    return render_template('prevention.html')


@app.route('/forum')
def forum():
    if "user" in session:
        return render_template('forum.html')
    else:
        return render_template('warning.html')


@app.route('/profile')
def profile():
    if "user" in session:
        return render_template('profile.html')
    else:
        return render_template('warning.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    else:
        username=request.form['username']
        password=request.form['password']
        person = Person.query.filter_by(username=username).first()
        if not person or not bcrypt.check_password_hash(person.password, password):
            flash('Please check your login details and try again', 'error') #'error' is optional
            return render_template('login.html')
        else:
            session['user'] = username
            session.permanent=True  # closing the browser will not log out
            flash('Logged in Successfully!')
            return redirect(url_for('profile'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username=request.form['username']
        email=request.form['email']
        # for added security when using bcrypt
        hashed_password=bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

        # check if this username is already taken
        person = Person.query.filter_by(username=username).first()
        if person:
            flash('This username already exist! Please choose another one!')
            return render_template('register.html')
        else:
            reg_details = (
                username,
                email,
                hashed_password,
            )
            add_users(reg_details)
            flash('Registration successful! Please login now.')
            return redirect(url_for('login')) # redirect from the current page to this page

# add the register user into our db
def add_users(reg_details):
    user = Person(username=reg_details[0], email=reg_details[1], password=reg_details[2])
    db.session.add(user)
    db.session.commit()


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)