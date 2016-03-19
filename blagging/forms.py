from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField

from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError

from .models import Author

class LoginForm(Form):
    username = StringField('Username: ', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

    def validate(self):
        return True