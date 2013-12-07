import datetime

from flask.ext.sqlalchemy import SQLAlchemy, BaseQuery as _BaseQuery
from flask.ext.cache import Cache

__all__ = [
    'db', 'cache', 'BaseQuery', 'SessionMixin'
]

db = SQLAlchemy()
cache = Cache()


class BaseQuery(_BaseQuery):
    pass


class SessionMixin(object):
    def to_dict(self, *columns):
        dct = {}
        for col in columns:
            value = getattr(self, col)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%Y-%m-%d %H:%M:%S')

            dct[col] = value
        return dct

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self
