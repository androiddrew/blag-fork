from flask import render_template, redirect, request, url_for
from flask_login import login_user, logout_user
from . import app, db, login_manager
from .models import Post, Tag, Author
from .forms import LoginForm


#Auth#################
@login_manager.user_loader
def load_user(userid):
    return Author.query.get(int(userid))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # login and validate the user:
        user = Author.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

#MAIN##############

@app.route('/')
@app.route('/index')
def index():
    return render_template('blog.html', new_posts=Post.newest(5), authors=Author.query.all())


@app.route('/post/<slug>')
def post(slug):
    post = Post.query.filter_by(display_title=slug).first_or_404()
    return render_template('post.html', post=post)


@app.route('/tag/<name>')
def tag(name):
    tag = Tag.query.filter_by(name=name).first_or_404()
    return render_template('tag.html', tag=tag)

#MAIN OTHER###########

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