import datetime

from .database import db, SessionMixin


class Account(db.Model, SessionMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120))

    created = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return '<Account %s>' % self.username


class Profile(db.Model, SessionMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    screen_name = db.Column(db.String(120), unique=True)
    location = db.Column(db.String(30))
    website = db.Column(db.String(100))
    description = db.Column(db.Text)

    def __repr__(self):
        return '<Profile %s>' % self.screen_name
