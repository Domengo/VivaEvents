from flask import Flask, request, flash, redirect, render_template, url_for
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask_httpauth import HTTPBasicAuth
from models.base_models import Base, User
import os, dotenv
import bcrypt
from form.registration import Registration
from form.login import Login
from flask_login import login_user


dotenv.load_dotenv()

app = Flask(__name__)
auth = HTTPBasicAuth()
SECRET_KEY = os.getenv('SECRET_KEY') or 'hard to guess string'
app.config['SECRET_KEY'] = SECRET_KEY


# Database configuration
event_user = os.getenv('eventU')
event_pwd = os.getenv('pwd')
event_host = os.getenv('host')
event_db = os.getenv('db')

engine = create_engine(f'mysql+mysqldb://{event_user}:{event_pwd}@{event_host}/{event_db}',echo=True)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """ Get user data from the form
    """
    form = Registration(request.form)
    if request.method == 'POST' and form.validate():
        password = form.password.data
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_user = User(email=form.email.data, password=hashed_password, username=form.username.data, phone=form.phone.data, fullname=form.fullname.data)

        if form.password.data != form.confirm_password.data:
            flash('Passwords do not match.')
            return render_template('signup.html')

        session = DBSession()
        session.add(new_user)
        flash('Thanks for registering')
        session.commit()


        return redirect('/login?message=success')
    return render_template('signup.html', form=form)

@auth.verify_password
def verify_password(email_or_username, password):
    """
    Find the user by email or username
    """
    session = DBSession()
    user = session.query(User).filter_by(email=email_or_username).first()

    if not user:
        # If user is not found by email, try finding by username
        user = session.query(User).filter_by(username=email_or_username).first()
    session.close()

    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return False
    return True



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if request.method == 'POST' and form.validate():
        email = form.email.data
        username = form.username.data
        password = form.password.data

        # Determine which field was used (email or username)
        email_or_username = email if email else username

        if verify_password(email_or_username, password):
            session = DBSession()
            user = session.query(User).filter_by(email=email_or_username).first() 
            #bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)
            login_user(user)
            flash('Login successful!')
            return redirect(url_for('landing_page'))
        else:
            flash('Invalid email/username or password')
            return render_template('login.html')
    return render_template('login.html', form=form)


@auth.login_required
@app.route('/landing_page', methods=['GET'])
def landing_page():
    return render_template('landing_page.html')
