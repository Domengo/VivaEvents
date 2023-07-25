from flask import Flask, request, flash, redirect, render_template, url_for, g, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from models.base_models import Base, User
import os, dotenv
import bcrypt
from form.registration import Registration
from form.login import Login


# Set up the logger

dotenv.load_dotenv()

app = Flask(__name__)
SECRET_KEY = os.getenv('SECRET_KEY') or 'hard to guess string'
app.config['SECRET_KEY'] = SECRET_KEY
app.config['PROPAGATE_EXCEPTIONS'] = True


# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database configuration
event_user = os.getenv('eventU')
event_pwd = os.getenv('pwd')
event_host = os.getenv('host')
event_db = os.getenv('db')

engine = create_engine(f'mysql+mysqldb://{event_user}:{event_pwd}@{event_host}/{event_db}', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

@login_manager.user_loader
def load_user(user_id):
    return db_session.query(User).get(int(user_id))

@app.before_request
def before_request():
    g.db_session = db_session()

@app.teardown_request
def teardown_request(exception=None):
    db_session.remove()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = Registration(request.form)
    if request.method == 'POST' and form.validate():
        if form.password.data != form.confirm_password.data:
            flash('Passwords do not match.')
            return render_template('signup.html', form=form)

        password = form.password.data
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_user = User(email=form.email.data, password=hashed_password, username=form.username.data, phone=form.phone.data, fullname=form.fullname.data)

        db_session.add(new_user)
        db_session.commit()

        flash('Thanks for registering')
        return redirect('/login?message=success')
    return render_template('signup2.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        # username = form.username.data
        password = form.password.data

        # Determine which field was used (email or username)
        # email_or_username = email if email else username

        if verify_password(email, password):
            user = db_session.query(User).filter_by(email=email).first()
            login_user(user)
            flash('Login successful!')
            return render_template('landing_page.html')
        else:
            flash('Invalid email/username or password')

    return render_template('login2.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/protected')
@login_required
def protected():
    return 'Logged in as: ' + current_user.username

def verify_password(email, password):
    user = db_session.query(User).filter(User.email == email).first()
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return False
    return True


if __name__ == "__main__":
    app.run(debug=True)
