# learnt from: https://youtu.be/71EU8gnZqZQ

from enum import unique
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy 
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
# from flask_wtf import wtforms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt # to hash our passwords

app = Flask(__name__)
db = SQLAlchemy(app) # creates the database instance
bcrpyt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # connects our app file to database
# adding secret code to the  app so that it secures the session cookie.
app.config['SECRET_KEY'] = 'thisisthesecretkey' # in any production environment or  if you have to deploy this, code should be secretive.

# going to allow our app and flask login to work together to handle things when logging in, loading users from ids etc.
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader # used to reload the user object from the user id stored in the session
def load_user(user_id):
    return User.query.get(int(user_id))


# Table for Database with 3 columns
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True) # max string length is 20 
    # and nullable=False means its a required field and cannot be empty, unique=True means every username should be unique
    password = db.Column(db.String(80), nullable=False) # password can be of max 80 characters once it's been hashed
# Now open REPL or open terminal
# type python
# then type from app import db
# then type db.create_all() # it will create all the tables that we have in our app file into our database
# then exit of the console (ctrl+d)
# to check whether the database is created or not
# type in the terminal, sqlite3 database.db
# then, .tables
# if the class name User come, means successfully created.

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    submit = SubmitField("Register")

    # we have provided in the database that username should be unique but not in the form, so:
    def validate_username(self, username):
        # this below will query the database that entered usrname is existing or not
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError("That username already exist. Please choose a different one.")
 
class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    submit = SubmitField("Login")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrpyt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return  redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required # we only access the dashboard if we're logged in, that's why @login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        # password is encrypted so that our registartion will be secure
        hashed_password = bcrpyt.generate_password_hash(form.password.data) # when anyone will submit the form, hashed password will be saved in database
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user) # added to database
        db.session.commit() # commit the changes
        return redirect(url_for('login'))
        # to check the user has registered or not, open terminal
        # type, sqlite3 database.db
        # then type, select * from user;
        
    return render_template('register.html', form=form)

if __name__=='__main__':
    app.run(debug=True)