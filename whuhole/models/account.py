import hashlib
from datetime import datetime
from werkzeug import security
from flask import current_app
from ._base import db, BaseQuery, SessionMixin

__all__ = ['Account', 'Profile']


class Account(db.Model, SessionMixin):
    query_class = BaseQuery

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, index=True,
                         nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    role = db.Column(db.String(10), default='new')
    active = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    created = db.Column(db.DateTime, default=datetime.utcnow)
    token = db.Column(db.String(20))

    def __init__(self, **kwargs):
        self.token = self.create_token(16)

        if 'password' in kwargs:
            raw = kwargs.pop('password')
            self.password = self.create_password(raw)

        if 'username' in kwargs:
            username = kwargs.pop('username')
            self.username = username.lower()

        if 'email' in kwargs:
            email = kwargs.pop('email')
            self.email = email.lower()

        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return self.screen_name or self.username

    def __repr__(self):
        return '<Account: %s>' % self.username

    @staticmethod
    def create_password(raw):
        pwd = '%s%s' % (raw, current_app.config.get('PASSWORD_SECRET'))
        return security.generate_password_hash(pwd)

    @staticmethod
    def create_token(length=16):
        return security.gen_salt(length)

    @property
    def is_staff(self):
        if self.id == 1:
            return True
        return self.role == 'staff' or self.role == 'admin'

    @property
    def is_admin(self):
        return self.id == 1 or self.role == 'admin'

    def check_password(self, raw):
        pwd = '%s%s' % (raw, current_app.config.get('PASSWORD_SECRET'))
        return security.check_password_hash(self.password, pwd)

    def change_password(self, raw):
        self.password = self.create_password(raw)
        self.token = self.create_token()

    def avator(self, size=48):
        md5email = hashlib.md5(self.email).hexdigest()
        query = '%s?s=%s' % (md5email, size)

        return current_app.config.get('GRAVATAR_BASE_URL') + query

    @property
    def profile(self):
        item = Profile.get_or_create(self.id)
        return item


class Profile(db.Model, SessionMixin):
    id = db.Column(db.Integer, primary_key=True)

    screen_name = db.Column(db.String(80))
    description = db.Column(db.String(400))
    city = db.Column(db.String(100))
    website = db.Column(db.String(100))

    @classmethod
    def get_or_create(self, uid):
        item = self.query.get(uid)
        if item:
            return item
        item = self(id=uid)
        db.session.add(item)
        return item
