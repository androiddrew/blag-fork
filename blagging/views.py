from datetime import datetime as dt
from flask import render_template, redirect, request, url_for, abort
from flask_login import login_user, logout_user, login_required, current_user, login_url
from . import app, db, login_manager
from .models import Post, Tag, Author, tags as Post_Tag
from .forms import LoginForm, PostForm


# Auth#################
@login_manager.user_loader
def load_user(userid):
    return Author.query.get(int(userid))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Author.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# MAIN##############

@app.route('/')
@app.route('/page/<int:page_num>')
def index(page_num=1):
    query = Post.query.filter(Post.published == True)
    pagination = query.order_by(Post.date.desc()).paginate(page=page_num, per_page=app.config['POST_PER_PAGE'],
                                                           error_out=True)
    return render_template('blog.html', pagination=pagination, authors=Author.query.all())


@app.route('/post/<slug>', methods=['GET', 'POST'])
def post(slug):
    post = Post.query.filter_by(_display_title=slug).filter(Post.published == True).first_or_404()
    return render_template('post.html', post=post)


@app.route('/tag/<name>')
@app.route('/tag/<name>/<int:page_num>')
def tag(name, page_num=1):
    tag = Tag.query.filter_by(name=name).first_or_404()
    query = Post.query.join(Post_Tag).join(Tag).filter(Tag.id == tag.id).filter(Post.published == True)
    pagination = query.filter(Post.published == True).order_by(Post.date.desc()).paginate(page=page_num,
                                                                                          per_page=app.config[
                                                                                              'POST_PER_PAGE'],
                                                                                          error_out=True)
    return render_template('tag.html', pagination=pagination, tag=tag)


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
        published = form.published.data
        post = Post(author=current_user, title=title, display_title=title, short_desc=short_desc, body=body, tags=tags,
                    published=published)
        with db.session.no_autoflush:
            db.session.add(post)
            db.session.commit()
        return redirect(url_for('index'))
    return render_template('post_form.html', form=form)


@app.route('/edit')
@login_required
def edit():
    posts = Post.query.filter(Post.author_id == current_user.id).order_by(Post.date.desc()).all()
    return render_template('edit_list.html', posts=posts)


@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != post.author:
        abort(403)
    form = PostForm(obj=post, post_id=post.id)
    if form.validate_on_submit():
        form.populate_obj(post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('post_form.html', form=form)


@app.route('/preview', methods=['GET', 'POST'])
@login_required
def preview_post():
    result = request.get_json(force=True)
    form_data = dict()
    form_data['date'] = dt.utcnow()
    form_data['author'] = current_user
    for field in result:
        form_data[field['name']] = field['value']
    form_data['tags'] = form_data.get('tags').split(',')
    return render_template('post_preview.html', post=form_data)


# MAIN OTHER###########
@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403


@app.errorhandler(404)  # bluprintname.app_errorhandler will register for the entire app when using blueprints
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    app.logger.error('Server Error: {}'.format(e))
    return render_template('500.html'), 500


@app.context_processor
def inject_tags():
    """context_processor similar to the app_context_processor for blueprints"""
    return dict(all_tags=Tag.all, tags_count=Tag.tag_count)


@app.context_processor
def inject_recent_posts():
    """context_processor similar to the app_context_processor for blueprints for recent posts"""
    return dict(recent_posts=Post.recent)


@app.context_processor
def inject_auth_url():
    return dict(auth_url=login_url)


@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    if fmt is None:
        fmt = '%Y-%m-%d'
    return date.strftime(fmt)
