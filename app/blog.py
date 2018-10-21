from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from app.auth import login_required

from flask_login import current_user, login_required

# from app.db import get_db

from . import db
from .models import Post

bp = Blueprint('blog', __name__)


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():

    # posts = Post.query.all()
    posts = db.session.query(Post). \
        filter(Post.author_id == g.user.id). \
        all()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post = Post(title=title,
                        body=body,
                        author_id=g.user.id)

            db.session.add(post)
            db.session.commit()
            flash('Successfully added a new post.')

            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


# def get_post(id, check_author=True):
#     # post = get_db().execute(
#     #     'SELECT p.id, title, body, created, author_id, username'
#     #     ' FROM post p JOIN user u ON p.author_id = u.id'
#     #     ' WHERE p.id = ?',
#     #     (id,)
#     # ).fetchone()
#
#
#
#     if post is None:
#         abort(404, "Post id {0} doesn't exist.".format(id))
#
#     if check_author and post['author_id'] != g.user['id']:
#         abort(403)
#
#     return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    # post = get_post(id)

    post = Post.query.get_or_404(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post.id = id
            post.title = title
            post.body = body
            db.session.commit()
            flash('Successfully edited the post.')

        return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('Successfully deleted the post.')

    return redirect(url_for('blog.index'))
