from flask_login import UserMixin, current_user
from app import db, login
from functools import wraps


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    role = db.Column(db.String(64), default='customer')

    def __repr__(self):
        return '<User {}>'.format(self.username)

@login.user_loader
def load_user(id):
    user = User.query.filter_by(id=id).first()
    return user


def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.role not in roles:
                # Redirect the user to an unauthorized notice!
                return "You are not authorized to access this page"
            return f(*args, **kwargs)
        return wrapped
    return wrapper

