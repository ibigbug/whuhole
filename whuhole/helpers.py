import hashlib

from flask import session


def login_user(user):
    uid = user.id
    token = user.token


def get_current_user():
    pass
