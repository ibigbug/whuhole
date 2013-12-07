import datetime
from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder
from werkzeug.datastructures import ImmutableDict


class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if hasattr(o, '__getitem__') and hasattr(o, 'keys'):
            # o is a dict
            return dict(o)
        if isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        return _JSONEncoder.default(self, o)


class Flask(_Flask):
    json_encoder = JSONEncoder

    jinja_options = ImmutableDict(
        extensions=[
            'jinja2.ext.autoescape',
            'jinja2.ext.do',
            'jinja2.ext.with_'
        ]
    )
