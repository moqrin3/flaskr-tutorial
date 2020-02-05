import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from app.auth import login_required

from app import storage
from flask_login import current_user, login_required
from datetime import datetime
from . import db, ALLOWED_EXTENSIONS
from .models import Post

bp = Blueprint('blog', __name__)
UPLOADS_FOLDER = "uploads"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_image_file(file):

    if not file:
        return None

    file.save(os.path.join(UPLOADS_FOLDER, file.filename))

    public_url = storage.upload_file(
        file.read(),
        file.filename,
        file.content_type
    )

    return public_url


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

        if 'img_file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['img_file']

        image_url = upload_image_file(file)

        if error is not None:
            flash(error)
        else:
            post = Post(title=title,
                        body=body,
                        created=created,
                        author_id=g.user.id,
                        file_url=image_url,
                        filename=file.filename)

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
        if 'img_file' in request.files:
            file = request.files['img_file']

            if file and allowed_file(file.filename):
                image_url = upload_image_file(request.files.get('img_file'))
            post.id = id
            post.title = title
            post.body = body
            post.file_url = image_url
            post.filename = file.filename
            db.session.commit()
            flash('Successfully edited the post.')
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
