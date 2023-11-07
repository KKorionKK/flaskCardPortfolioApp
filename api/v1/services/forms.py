from flask_wtf import FlaskForm
from wtforms.validators import Email
from wtforms import StringField, PasswordField, SelectField, FileField
from api.v1.services.consts import countries


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[Email()])
    password = PasswordField("Password", validators=[])


class RegisterForm(LoginForm):
    name = StringField("Name", validators=[])
    username = StringField("Username", validators=[])

class CreateForm(FlaskForm):
    header = StringField("Header")
    content = StringField("Content")
    link = StringField("Link")
    emoji = SelectField("emoji", choices=countries)
    picture = FileField("Picture")
