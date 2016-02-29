from datetime import datetime as dt
import re
from sqlalchemy import desc
from . import db

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String(25), unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    date = db.Column(db.DateTime, default=dt.utcnow)
    title = db.Column(db.String(80), nullable=False)
    display_title = db.Column(db.String(80), nullable=False, unique=True)
    short_desc = db.Column(db.String(200))
    body = db.Column(db.String)

    @staticmethod
    def newest(num):
        """Returns a list of posts"""
        return Post.query.order_by(desc(Post.date)).limit(num)

    @staticmethod
    def slugify(text, demlim='-'):
        """Generates an ASCII-only slug."""
        result = [word for word in _punct_re.split(text.lower())]
        return demlim.join(result)
