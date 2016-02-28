from flask import render_template

from . import app, db
from .models import Post


@app.route("/")
@app.route('/index')
def index():
    return render_template('blog.html', new_posts=Post.newest(5))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500 # Debug needs to be turned off to hit a 500