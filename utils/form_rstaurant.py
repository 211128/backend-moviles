from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, EqualTo



class RegiterForm(FlaskForm):
    name = StringField('name', validators=[InputRequired()])
    email = StringField('email', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
    name_department= StringField('name_department', validators=[InputRequired()])
    description = StringField('description', validators=[InputRequired()])
    contacto = StringField('contacto', validators=[InputRequired()])

class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
    