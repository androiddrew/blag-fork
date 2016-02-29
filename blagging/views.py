from flask import render_template

from . import app, db
from .models import Post


@app.route('/')
@app.route('/index')
def index():
    return render_template('blog.html', new_posts=Post.newest(5))

"""
@app.route('/post/<int:postid>')
def post(postid):
    post = Post.query.filter_by(id=postid).first_or_404()
    return render_template('post.html', post=post)
"""
@app.route('/post/<slug>')
def post(slug):
    post = Post.query.filter_by(display_title=slug).first_or_404()
    return render_template('post.html', post=post)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500 # Debug needs to be turned off to hit a 500