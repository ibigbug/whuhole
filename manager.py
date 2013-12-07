import gevent.monkey
gevent.monkey.patch_all()

import os
import sys
from flask_script import Manager
from whuhole.app import create_app

settings = os.path.abspath('./etc/dev_config.py')
if 'WHUHOLE_SETTINGS' not in os.environ:
    os.environ['WHUHOLE_SETTINGS'] = settings

app = create_app()
manager = Manager(app)


@manager.command
def runserver(port=3000):
    """start a local server for development"""

    from flask import send_from_directory
    from gevent.wsgi import WSGIServer
    from werkzeug.serving import run_with_reloader
    from werkzeug.debug import DebuggedApplication

    port = int(port)

    @app.route('/static/<path:filename>')
    def static_file(filename):
        datadir = os.path.abspath('public/static')
        return send_from_directory(datadir, filename)

    wsgi = DebuggedApplication(app)

    @run_with_reloader
    def run_server():
        print('start server at: 127.0.0.1:%s' % port)

        http_server = WSGIServer(('', port), wsgi)
        http_server.serve_forever()

    try:
        run_server()
    except (KeyboardInterrupt):
        sys.exit()

@manager.command
def syncdb():
    from whuhole.models import db
    from whuhole.models import hole
    db.init_app(app)
    db.create_all()


if __name__ == '__main__':
    manager.run()
