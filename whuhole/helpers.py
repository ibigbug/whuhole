# coding: utf-8
import functools

from flask import session
from flask import g
from flask import url_for
from flask import request
from flask import redirect
from flask import jsonify
from flask import flash

from models import Account


def login_user(user):
    uid = user.id
    token = user.token
    session['uid'] = uid
    session['token'] = token
    return user


def logout_user():
    session.pop('uid', None)
    session.pop('token', None)


def get_current_user():
    logined = 'uid' in session and 'token' in session
    if not logined:
        return None
    uid = session['uid']
    user = Account.query.filter_by(id=uid).first()
    if not user:
        return None
    return user


def login_required(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        if not g.user:
            if request.is_xhr:
                return jsonify(stat='fail', message=u'请登录再操作')
            url = url_for('account.login')
            if '?' not in url:
                url += '?next=' + request.url
            flash(u'请登录后再操作', 'info')
            return redirect(url)

        return method(*args, **kwargs)
    return wrapper
