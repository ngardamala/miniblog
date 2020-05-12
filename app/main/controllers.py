from flask import current_app
from datetime import datetime
from flask import Blueprint
from app.database import db
from flask_login import current_user, login_required
from flask import render_template, flash, redirect, url_for, request
from .forms import PostForm, EditProfileForm
from .models import Post
from app.auth.models import User

module = Blueprint('main', __name__)


@module.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@module.route('/', methods=['GET', 'POST'])
@module.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('main/index.html', title='Home',
                           form=form, posts=posts.items,
                           next_url=next_url,
                           prev_url=prev_url)


@module.route('/user/<id>')
@login_required
def user(id):
    user = User.query.filter_by(id=id).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', id=user.id, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.user', id=user.id, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('main/user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@module.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('main/edit_profile.html', title='Edit Profile',
                           form=form)


@module.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('main/index.html', title='Explore',
                           posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@module.route('/follow/<id>')
@login_required
def follow(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        flash('User with id {} not found.'.format(id))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('main.user', id=id))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(user.username))
    return redirect(url_for('main.user', id=id))


@module.route('/unfollow/<id>')
@login_required
def unfollow(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        flash('User with id {} not found.'.format(id))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('main.user', id=id))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(user.username))
    return redirect(url_for('main.user', id=id))


@module.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@module.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500
