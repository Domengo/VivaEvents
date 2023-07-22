from wtforms import Form, StringField, PasswordField, validators

class Registration(Form):
    fullname = StringField('fullname', [
        validators.Length(min=4, max=50), validators.input_required()])
    username = StringField('username', [validators.Length(min=4, max=50)])
    email = StringField('email', [validators.Length(min=4, max=50)]) #validators.Email()
    password = PasswordField('password', [
        validators.Length(min=4, max=50), validators.InputRequired(),
        validators.EqualTo('confirm_password', message="password must match")])
    phone = StringField('phone', [validators.Length(min=4, max=50)])
    confirm_password = PasswordField('password', [
        validators.Length(min=4, max=50)])


# def user(request):
#     form = Registration(request.POST)
#     if request.method == 'POST' and form.validate:
#         fullname = form.fullname.data
#         username = form.usernamename.data
#         email = form.email.data
#         password = form.password.data
#         phone = form.phone.data
#         confirm_password = form.confirm_password.data
#         return redirect('signup')
#     return render_template('signup.html', form=form)

# u = user(request.form)

