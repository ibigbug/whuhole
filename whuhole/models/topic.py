import datetime
from .database import db, SessionMixin


class Topic(db.Model, SessionMixin):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

    created = db.Column(db.DateTime, default=datetime.datetime.now)
    updated = db.Column(db.DateTime, default=datetime.datetime.now)

    up = db.Column(db.Integer, default=0)
    down = db.Column(db.Integer, default=0)
    reply_count = db.Column(db.Integer, default=0)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    reply = db.relationship('Reply', backref='topic',
                            lazy='dynamic')

    def __repr__(self):
        return '<Topic %s>' % self.id


class Reply(db.Model, SessionMixin):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)

    created = db.Column(db.DateTime, default=datetime.datetime.now)
    updated = db.Column(db.DateTime, default=datetime.datetime.now)

    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))

    up = db.Column(db.Integer, default=0)
    down = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Reply %s>' % self.id
