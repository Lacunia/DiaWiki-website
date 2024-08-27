from flask import Flask, render_template, request, flash, redirect, url_for, session, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, DateTime
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt, check_password_hash
from io import BytesIO

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
    pfp = db.Column(db.LargeBinary)
    topic = db.relationship('Topic', backref='person', lazy=True, uselist=False)
    comment = db.relationship('Comment', backref='person', lazy=True, uselist=False)

class Topic(db.Model):
    __tablename__ = 'Topic'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String)
    username = db.Column(db.String(20), db.ForeignKey('Person.username'), nullable=False) 
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    like = db.Column(db.Integer, nullable=False, default=0)

class Comment(db.Model):
    __tablename__ = 'Comment'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, unique=True, nullable=False)
    topicId = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(20), db.ForeignKey('Person.username'), nullable=False) 
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    like = db.Column(db.Integer, nullable=False, default=0)

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
        topics = Topic.query.order_by(desc(Topic.date)).all()
        return render_template('forum.html', topics=topics)
    else:
        return render_template('warning.html')


@app.route('/add_topic', methods=["GET", "POST"])
def add_topic():
    if "user" in session:
        # add a new topic/post
        if request.method == "POST":
            topic = Topic(
                title=request.form["title"],
                description=request.form["description"],
                username=session.get('user')
            )
            db.session.add(topic)
            db.session.commit()
        return render_template('add_topic.html')
    else:
        return render_template('warning.html')
    

@app.route('/topic/<int:id>', methods=["GET", "POST"])
def topic(id):
    if "user" in session:
        # add a new comment
        if request.method == "POST":
            comment = Comment(
                text=request.form["comment"],
                topicId=id,
                username=session.get('user'),
            )
            db.session.add(comment)
            db.session.commit()
        topic = Topic.query.filter_by(id=id).first()
        comments = Comment.query.filter_by(topicId=id).order_by(desc(Comment.date)).all()
        return render_template('topic.html', topic=topic, comments=comments)
    else:
        return render_template('warning.html')


@app.route('/add_like/<int:id>')
def add_like(id):
    topic = Topic.query.filter_by(id=id).first()
    if topic:
        topic.like += 1
    db.session.commit()
    return redirect(url_for('topic', id=id))


@app.route('/profile')
def profile():
    if "user" in session:
        # get the username and email of the user and send it to the html page
        username = session['user']
        user = Person.query.filter_by(username=username).first()
        return render_template('profile.html', user=user)
    else:
        return render_template('warning.html')


# this route is for uploading pfp picture into the database
@app.route('/upload', methods=['POST'])
def upload():
    if 'user' not in session:
        return redirect(url_for('login'))

    user = Person.query.filter_by(username=session['user']).first()
    # the following get the user to choose a picture from their laptop and upload it into the database
    file = request.files['pfp']
    if file:
        # set the value of this attribute to the file (picture) that we just chose
        user.pfp = file.read()
        db.session.commit()
        flash('Profile picture updated successfully')
        return redirect(url_for('profile'))
    # else
    flash('No file selected for upload', 'error')
    return redirect(url_for('profile'))


@app.route('/get_pfp/<username>')
def get_pfp(username):
    user = Person.query.filter_by(username=username).first()
    # if the user and their pfp both exists and are not null, then show the stored pfp
    # otherwise, use the general pic
    if user and user.pfp:
        return send_file(BytesIO(user.pfp), mimetype='image/jpeg')
    return send_file('static/img/general-pfp.jpg', mimetype='image/jpeg')


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