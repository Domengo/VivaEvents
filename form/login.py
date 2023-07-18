from wtforms import Form, StringField, PasswordField, validators

class Login(Form):
    email = StringField('email', [validators.Length(min=4, max=50)]) #validators.Email()
    username = StringField('username', [validators.Length(min=4, max=50)])
    password = PasswordField('password', [
        validators.Length(min=4, max=50), validators.InputRequired()])
