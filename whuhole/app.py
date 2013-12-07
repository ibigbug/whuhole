import os
import logging
import time

from ._flask import Flask
from flask import g
from flask.ext.babel import Babel

from models import db
from helpers import get_current_user


def create_app(config=None):
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static'
    )

    app.config.from_pyfile('_settings.py')

    if 'WHUHOLE_SETTINGS' in os.environ:
        app.config.from_envvar('WHUHOLE_SETTINGS')

    if isinstance(config, dict):
        app.config.update(config)
    elif config:
        app.config.from_pyfile(config)

    @app.before_request
    def load_current_user():
        g.user = get_current_user()
        if g.user and g.user.is_staff:
            g._before_request_time = time.time()

    @app.after_request
    def rendering_time(response):
        if hasattr(g, '_before_request_time'):
            delta = time.time() - g._before_request_time
            response.headers['X-Render-Time'] = delta
        return response

    db.init_app(app)
    register_bp(app)
    register_logger(app)
    Babel(app)

    return app


def register_bp(app):
    from .views import hole, account, front
    app.register_blueprint(hole.bp, url_prefix='/-/hole')
    app.register_blueprint(account.bp, url_prefix='/-/user')
    app.register_blueprint(front.bp, url_prefix='')

    return app


def register_logger(app):
    if app.debug:
        return
    handler = logging.StreamHandler()
    handler.setLevel(logging.ERROR)
    app.logger.addHandler(handler)

if __name__ == '__main__':
    app = create_app()
    app.run(port=3000)
