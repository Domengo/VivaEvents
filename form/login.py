from wtforms import StringField, PasswordField, SubmitField, validators
from flask_wtf import FlaskForm
class Login(FlaskForm):
    email = StringField('email', [validators.Length(min=4, max=50)]) #validators.Email()
    username = StringField('username', [validators.Length(min=4, max=50)])
    password = PasswordField('password', [
        validators.Length(min=4, max=50), validators.InputRequired()])
    submit = SubmitField('submit')
