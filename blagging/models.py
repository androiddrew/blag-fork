from datetime import datetime as dt
import re
from sqlalchemy import desc
from sqlalchemy.orm import relationship, backref
from . import db

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

tags = db.Table('post_tag',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                db.Column('post_id', db.Integer, db.ForeignKey('post.id')))


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    display_name = db.Column(db.String(25), unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic') #Adding this allowed me to use author as a parameter to the Comment constructor


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    date = db.Column(db.DateTime, default=dt.utcnow)
    title = db.Column(db.String(80), nullable=False)
    display_title = db.Column(db.String(80), nullable=False, unique=True, index=True)
    short_desc = db.Column(db.String(200))
    body = db.Column(db.String)
    # secondary setups the link table between Tag and Post backref add a post attribute to the Tag
    _tags = db.relationship('Tag', secondary=tags, backref=db.backref('posts',
                                                                      lazy='dynamic'))
    comments = db.relationship('Comment', backref=db.backref('post', lazy='joined') )# leave lazy loading off

    @staticmethod
    def newest(num):
        """Returns a list of posts"""
        return Post.query.order_by(desc(Post.date)).limit(num)

    @staticmethod
    def slugify(text, demlim='-'):
        """Generates an ASCII-only slug."""
        result = [word for word in _punct_re.split(text.lower())]
        return demlim.join(result)

    @property
    def tags(self):
        return ",".join([t.name for t in self._tags])

    @tags.setter
    def tags(self, string):
        if string:
            self._tags = [Tag.get_or_create(name) for name in string.split(',')]
        else:
            self._tags = []


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    date = db.Column(db.DateTime, default=dt.utcnow)
    text = db.Column(db.String, nullable=False)
    # Sets up an Adjacency List Relationship for comments to be self referential
    # parent_id = db.Column(db.Integer(), db.ForeignKey('comment.id'))
    # children = relationship("Comment", backref=backref('parent', remote_side=[id]), lazy='joined', join_depth=2)


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

    def __repr__(self):
        return self.name