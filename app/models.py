from app import db, login_manager
from flask_login import UserMixin


class User(UserMixin, db.Model):
    """
    Create an User table
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Post(db.Model):
    """
    Create a Post table
    """
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created = db.Column(db.TIMESTAMP, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.String(200), nullable=False)
