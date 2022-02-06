import flask
from functools import wraps
from models.login.user_class import User


def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        user = User.current()
        if not user.is_login:
            return flask.redirect('/')
        return func(*args, **kwargs)
    return inner
