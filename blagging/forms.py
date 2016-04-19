from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField

from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError

from .models import Author, Post


class LoginForm(Form):
    username = StringField('Username: ', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')

    def validate(self):
        return True


class PostForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    published = SelectField('Status', choices=[('1', 'Published'), ('0', 'Draft')], validators=[DataRequired()])
    short_desc = TextAreaField("Front page display", validators=[DataRequired()])
    body = TextAreaField("What's on your mind?", validators=[DataRequired()])
    tags = StringField('Tags')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        if 'post_id' in kwargs:
            self.post_id = kwargs['post_id']
        else:
            self.post_id = None

    def validate_title(self, title_field):
        post = Post.query.filter_by(title=title_field.data).first()
        if post and post.id != self.post_id:
            raise ValidationError('This title has already been used.')


class CommentForm(Form):
    text = TextAreaField("Leave a comment", validators=[DataRequired()])