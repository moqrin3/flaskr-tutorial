from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from app.auth import login_required

from flask_login import current_user, login_required
from datetime import datetime
from . import db
from .models import Post

bp = Blueprint('blog', __name__)


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():

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
        created = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post = Post(title=title,
                        body=body,
                        created=created,
                        author_id=g.user.id)

            db.session.add(post)
            db.session.commit()
            flash('Successfully added a new post.')

            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):

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
