from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators


class LoginForm(FlaskForm):
    username = StringField('Brugernavn', [validators.DataRequired()])
    password = PasswordField('Kodeord', [validators.DataRequired()])