from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    origin = SelectField('Origin')
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class searchForm(FlaskForm):
    origin = SelectField(u'Origin', coerce=str, choices=[])
    destination = SelectMultipleField("Destination", coerce=str, choices=[])
    submit = SubmitField('Search')