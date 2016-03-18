from flask import render_template

from . import app, db
from .models import Post, Tag, Author


@app.route('/')
@app.route('/index')
def index():
    return render_template('blog.html', new_posts=Post.newest(5), authors=Author.query.all())


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

@app.context_processor
def inject_tags():
    """context_processor similar to the app_context_processor for blueprints"""
    return dict(all_tags=Tag.all)