import os

from flask import Flask

from models import db


def create_app():
    app = Flask(__name__)
    app.config.from_object('whuhole.settings')

    if 'WHUHOLE_SETTINGS' in os.environ:
        app.config.from_envvar('WHUHOLE_SETTINGS')

    db.init_app(app)

    return app


def main():
    app = create_app()
    app.run(port=3000)


if __name__ == '__main__':
    main()
