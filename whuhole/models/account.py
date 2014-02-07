import datetime

from werkzeug.security import generate_password_hash

from .database import db, SessionMixin


class Account(db.Model, SessionMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120))
    token = db.Column(db.String(120))

    created = db.Column(db.DateTime, default=datetime.datetime.now)
    updated = db.Column(db.DateTime, default=datetime.datetime.now)

    profile = db.relationship('Profile', uselist=False, backref='account')
    topic = db.relationship('Topic', backref='account', lazy='dynamic')
    reply = db.relationship('Reply', backref='account', lazy='dynamic')
    like = db.relationship('Like', backref='account', lazy='dynamic')

    def set_password(self):
        if not self.password:
            raise ValueError('No password set')
        password_hash = generate_password_hash(self.password)
        _, salt, __ = password_hash.split('$')
        self.token = salt
        self.password = password_hash

        # must save user manully

    def __repr__(self):
        return '<Account %s>' % self.username


class Profile(db.Model, SessionMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    screen_name = db.Column(db.String(120), unique=True)
    location = db.Column(db.String(30))
    website = db.Column(db.String(100))
    description = db.Column(db.Text)

    created = db.Column(db.DateTime, default=datetime.datetime.now)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))

    def __repr__(self):
        return '<Profile %s>' % self.screen_name
