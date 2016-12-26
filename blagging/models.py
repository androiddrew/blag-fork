from datetime import datetime as dt
import re
from sqlalchemy import desc, func
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from . import db

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

tags = db.Table('post_tag',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                db.Column('post_id', db.Integer, db.ForeignKey('post.id')))


class Author(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    display_name = db.Column(db.String(25), unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    password_hash = db.Column(db.String)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        return Author.query.filter_by(display_name=username).first()

    def __repr__(self):
        return '<User: %r >' % self.display_name



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    date = db.Column(db.DateTime, default=dt.utcnow)
    date_modified = db.Column(db.DateTime, default=dt.utcnow, onupdate=dt.utcnow)
    title = db.Column(db.String(80), nullable=False)
    _display_title = db.Column(db.String(80), nullable=False, unique=True, index=True)
    published = db.Column(db.Boolean, nullable=False, default=True)
    short_desc = db.Column(db.String(200))
    body = db.Column(db.String)
    # secondary setups the link table between Tag and Post backref add a post attribute to the Tag
    _tags = db.relationship('Tag', secondary=tags, backref=db.backref('posts',
                                                                      lazy='dynamic'))

    @staticmethod
    def newest(num):
        """Returns a list of posts"""
        return Post.query.order_by(desc(Post.date)).limit(num)

    @property
    def display_title(self):
        return self._display_title

    @display_title.setter
    def display_title(self, text, demlim='-'):
        """Generates an ASCII-only slug."""
        result = [word for word in _punct_re.split(text.lower())]
        self._display_title = demlim.join(result)

    @property
    def tags(self):
        return ",".join([t.name for t in self._tags])

    @tags.setter
    def tags(self, string):
        if string:
            self._tags = [Tag.get_or_create(name) for name in string.split(',')]
        else:
            self._tags = []

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False, unique=True, index=True)

    @staticmethod
    def get_or_create(name):
        try:
            return Tag.query.filter_by(name=name).one()
        except:
            return Tag(name=name)

    @staticmethod
    def all():
        return Tag.query.all()

    @staticmethod
    def tag_count():
        """Return the Tag and the count of tags for display in the catergories section"""
        return db.session.query(Tag, func.count(tags.c.tag_id)).join(tags, Tag.id==tags.c.tag_id).group_by(Tag.name).all()

    def __repr__(self):
        return self.name
