from datetime import datetime
from ._base import db, BaseQuery, SessionMixin

__all__ = ['Status', 'StatusReply', 'StatusLike']


class Status(db.Model, SessionMixin):
    query_class = BaseQuery

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, nullable=False, index=True)

    content = db.Column(db.Text)

    likes = db.Column(db.Integer, default=0)
    reply_count = db.Column(db.Integer, default=0)

    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __str__(self):
        return self.content[:10]

    def __repr__(self):
        return '<Status: %s>' % self.id

    def save(self, user=None):
        if self.id:
            db.session.add(self)
            db.session.commit()

            return self

        if user:
            self.account_id = user.id
            user.active = datetime.utcnow()
            db.session.add(user)

        db.session.add(self)
        db.session.commit()

        return self


class StatusReply(db.Model):
    query_class = BaseQuery

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, nullable=False)
    status_id = db.Column(db.Integer, index=True, nullable=False)
    content = db.Column(db.Text)

    created = db.Column(db.DateTime, default=datetime.utcnow)

    def save(self):
        if self.id:
            db.session.add(self)
            db.session.commit()

            return self

    def delete(self, user=None, status=None):
        if not status:
            status = Status.query.get(self.status_id)

        status.reply_count -= 1
        db.session.add(status)
        db.session.delete(self)
        db.session.commit()

        return self


class StatusLike(db.Model):
    query_class = BaseQuery

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, nullable=False)
    status_id = db.Column(db.Integer, index=True, nullable=False)

    created = db.Column(db.DateTime, default=datetime.utcnow)

    def save(self):
        if self.id:
            db.session.add(self)
            db.session.commit()

            return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

        return self
