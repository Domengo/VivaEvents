from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Create a new User instance
        user = User(username=username, password_hash=password)

        # Add the user to the session and commit to the database
        db.session.add(user)
        db.session.commit()

        return redirect('/login')

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verify user credentials
        user = User.query.filter_by(username=username, password_hash=password).first()

        if user:
            session['user_id'] = user.id
            return redirect('/dashboard')

        return redirect('/login')

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    # Retrieve user information from session
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        return f"Welcome, {user.username}!"
    else:
        return redirect('/login')


if __name__ == '__main__':
    app.run()
