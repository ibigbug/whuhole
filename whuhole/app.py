import os

from flask import Flask
from flask import g

from helpers import get_current_user
from models import db


def create_app():
    app = Flask(
        __name__,
        template_folder='templates'
    )
    app.config.from_object('whuhole.settings')

    if 'WHUHOLE_SETTINGS' in os.environ:
        app.config.from_envvar('WHUHOLE_SETTINGS')

    db.init_app(app)
    register_routes(app)

    @app.before_request
    def load_current_user():
        g.user = get_current_user()

    return app


def register_routes(app):
    from views import api
    from views import account
    from views import front
    from views import topic

    app.register_blueprint(api.bp, url_prefix='/api')
    app.register_blueprint(account.bp, url_prefix='/account')
    app.register_blueprint(front.bp, url_prefix='/')
    app.register_blueprint(topic.bp, url_prefix='/topic')


def main():
    app = create_app()
    app.run(port=3000)


if __name__ == '__main__':
    main()
