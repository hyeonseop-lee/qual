from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length

class LoginForm(Form):
    username = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(Form):
    username = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=4)])
    confirm = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')])
    registerkey = PasswordField('Register Key', validators=[DataRequired()])
