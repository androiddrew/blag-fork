from flask import render_template

from . import app, db
from .models import Post

@app.route("/")
@app.route('/index')
def index():
    return render_template('blog.html', new_posts=Post.newest(5))

