import os

from flask import Flask

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

    return app


def register_routes(app):
    from views import api
    from views import account

    app.register_blueprint(api.bp, url_prefix='/api')
    app.register_blueprint(account.bp, url_prefix='/account')


def main():
    app = create_app()
    app.run(port=3000)


if __name__ == '__main__':
    main()
