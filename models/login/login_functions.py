import flask
import os
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


def change_file_name(file_path: str, file_name_find: str, new_file_name) -> bool:
    """
    :param file_path: file path to search
    :param file_name_find: file name to find
    :param new_file_name: file name to change
    :return:True when file name was change
    """
    for f in os.listdir(file_path):
        if f.startswith(file_name_find):
            old_file = os.path.join(file_path, f)
            new_file = os.path.join(file_path, new_file_name + "." + f.split(".")[-1])
            os.rename(old_file, new_file)
            return True
    return False


def remove_file(file_path: str, file_name_find: str) -> bool:
    """
    :param file_path: file path to search
    :param file_name_find: file name to find
    :return:True when file file_name was deleted
    """
    for f in os.listdir(file_path):
        if f.startswith(file_name_find):
            os.remove(os.path.join(file_path, f))
            return True
    return False
