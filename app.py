from flask import Flask, request, jsonify, make_response, redirect, render_template
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask_httpauth import HTTPBasicAuth
from models.base_models import Base, User
import bcrypt

app = Flask(__name__)
auth = HTTPBasicAuth()

# Database configuration
engine = create_engine('mysql+mysqldb://eventU:pwd@host/event_db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)


@app.route('/signup', methods=['POST'])
def signup():
    # Get user data from the form
    name = request.form.get('name')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Create a new user
    new_user = User(name=name, username=username, email=email, password=hashed_password)

    # Store the user in the database
    session = DBSession()
    session.add(new_user)
    session.commit()

    return redirect('/login?message=success')


@app.route('/login')
def login():
    message = request.args.get('message')
    return render_template('login.html', message=message)


@auth.verify_password
def verify_password(email_or_username, password):
    # Find the user by email or username
    session = DBSession()
    user = session.query(User).filter_by(email=email_or_username).first()

    if not user:
        # If user is not found by email, try finding by username
        user = session.query(User).filter_by(username=email_or_username).first()

    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return False

    return True


@app.route('/protected')
def protected():
    # Get the token from the cookie
    token = request.cookies.get('token')

    # Verify the token and retrieve the user
    email_or_username = auth.verify_password(token, '')

    if not email_or_username:
        return jsonify({'message': 'Authentication failed.'}), 401

    # Authentication successful
    return jsonify({'message': 'Protected resource.'})


if __name__ == '__main__':
    app.run(debug=True)
