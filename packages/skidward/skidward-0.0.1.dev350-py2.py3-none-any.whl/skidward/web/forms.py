from wtforms import StringField, PasswordField, validators
from wtforms.fields.html5 import EmailField
from flask_wtf import FlaskForm
from flask_security.forms import LoginForm


class TaskContextForm(FlaskForm):
    key = StringField("Key", [validators.DataRequired()])
    value = StringField("Value", [validators.DataRequired()])


class SkidwardLoginForm(LoginForm):
    email = EmailField(
        "Email ID", validators=[validators.DataRequired(), validators.Email()]
    )
    password = PasswordField("Password", validators=[validators.DataRequired()])
