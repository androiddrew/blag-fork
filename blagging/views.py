from flask import render_template, redirect, request, url_for, abort
from flask_login import login_user, logout_user, login_required, current_user
from . import app, db, login_manager
from .models import Post, Tag, Author
from .forms import LoginForm, PostForm


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


@app.route('/author/<display_name>')
def user(display_name):
    user = Author.query.filter_by(display_name=display_name).first_or_404()
    return render_template('author.html', author=user)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        short_desc = form.short_desc.data
        body = form.body.data
        tags = form.tags.data
        post = Post(author=current_user, title=title, short_desc=short_desc, body=body, tags=tags,
                    display_title=Post.slugify(title))
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('post_form.html', form=form)


@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != post.author:
        abort(403)
    form = PostForm(obj=post)
    if form.validate_on_submit():
        form.populate_obj(post)
        db.session.commit()
        return redirect(url_for('post', slug=post.display_title))
    return render_template('post_form.html', form=form)

#MAIN OTHER###########

@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403


@app.errorhandler(404) # bluprintname.app_errorhandler will register for the entire app when using blueprints
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500 # Debug needs to be turned off to hit a 500

@app.context_processor
def inject_tags():
    """context_processor similar to the app_context_processor for blueprints"""
    return dict(all_tags=Tag.all)