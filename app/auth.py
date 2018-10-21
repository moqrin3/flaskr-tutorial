import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from . import db
from .models import User

# 追記
from flask_login import login_required, login_user, logout_user

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password = generate_password_hash(password)
        # db = get_db()

        user = User(username=username,
                    password=password)

        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        # elif db.execute(
        #         'SELECT id FROM user WHERE username = ?', (username,)
        # ).fetchone() is not None:
        #     error = 'User {} is already registered.'.format(username)

        if error is None:
            # db.execute(
            #     'INSERT INTO user (username, password) VALUES (?, ?)',
            #     (username, generate_password_hash(password))
            # )
            # db.commit()

            db.session.add(user)
            db.session.commit()
            flash('Successfully added a new user.')

            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # # db = get_db()
        #
        user = User.query.filter_by(username=username).first()
        # print(user.username)
        #
        error = None
        # # user = db.execute(
        # #     'SELECT * FROM user WHERE username = ?', (username,)
        # # ).fetchone()
        #
        # # if user is not None and user.verify_password(
        # #         password):
        # # login_user(user)
        #
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'
        #
        if error is None:
            session.clear()
            session['user_id'] = user.id
            login_user(user)
            return redirect(url_for('index'))

        flash('Invalid email or password.')
        # flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    session.clear()
    logout_user()
    flash('Logged out.')

    # redirect to the login page
    return redirect(url_for('auth.login'))

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)
        # g.user = get_db().execute(
        #     'SELECT * FROM user WHERE id = ?', (user_id,)
        # ).fetchone()

# @bp.route('/logout')
# def logout():
#     session.clear()
#     return redirect(url_for('index'))
#
#
# def login_required(view):
#     @functools.wraps(view)
#     def wrapped_view(**kwargs):
#         if g.user is None:
#             return redirect(url_for('auth.login'))
#
#         return view(**kwargs)
#
#     return wrapped_view


# if __name__ == '__main__':
#     app.run(debug=True)
