from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField, TextAreaField

from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError

from .models import Author


class LoginForm(Form):
    username = StringField('Username: ', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')

    def validate(self):
        return True


class PostForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    short_desc = TextAreaField("Front page display", validators=[DataRequired()])
    body = TextAreaField("What's on your mind?", validators=[DataRequired])
    tags = StringField('Tags')

    def validate(self):
        return True