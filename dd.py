def solution(A):
    # 1. Initialize a set to store all the elements in A.
    s = set()
    for i in range(len(A)):
        s.add(A[i])
    # 2. Iterate over all the integers from 1 to 1000000.
    # If an integer is not in the set, then return it.
    for i in range(1, 1000001):
        if i not in s:
            return i
    # 3. If all the integers from 1 to 1000000 are in the set, then return 1.
    return 1

A = [-1, -3]
print(solution(A))

from flask import Flask, request, flash, redirect, render_template, url_for
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask_httpauth import HTTPBasicAuth
from models.base_models import Base, User
import os, dotenv
import bcrypt
from form.registration import Registration

dotenv.load_dotenv()

app = Flask(__name__)
auth = HTTPBasicAuth()
SECRET_KEY = os.getenv('SECRET_KEY') or 'hard to guess string'
app.config['SECRET_KEY']


# Database configuration
# ... (Your database configuration code here) ...

# ... (Your signup route here) ...

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Retrieve the user from the database based on the provided email
        session = DBSession()
        user = session.query(User).filter_by(email=email).first()
        session.close()

        # Check if the user exists and the password is correct
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            # You can use a session or token-based authentication to keep the user logged in
            # For simplicity, here we'll just use a flash message to indicate successful login
            flash('Login successful!')
            return redirect('/dashboard')  # Redirect to the dashboard page after successful login

        # If the user doesn't exist or the password is incorrect, show an error message
        flash('Invalid email or password. Please try again.')

    return render_template('login.html')  # Render the login page template

# ... (Other routes and functions) ...

@auth.verify_password
def verify_password(email_or_username, password):
    """
    Find the user by email or username and verify the password
    """
    session = DBSession()
    user = session.query(User).filter((User.email == email_or_username) | (User.username == email_or_username)).first()
    session.close()

    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return False
    return True

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        
        email_or_username = email or username

        if verify_password(email_or_username, password):
            flash('Login successful!')
            return redirect('/landing_page?message=success')
        else:
            flash('Invalid email/username or password')
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)
