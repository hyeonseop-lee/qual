from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length

class LoginForm(Form):
    username = TextField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class RegisterForm(Form):
    username = TextField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[Length(min=4)])
    confirm = PasswordField('confirm', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')])
