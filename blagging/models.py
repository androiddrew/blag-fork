from datetime import datetime as dt
from sqlalchemy import desc
from . import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=dt.utcnow)
    title = db.Column(db.String(80))
    short_desc = db.Column(db.String(200))
    body = db.Column(db.String)

    @staticmethod
    def newest(num):
        return Post.query.order_by(desc(Post.date)).limit(num)