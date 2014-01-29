import os
import sys

from flask.ext.script import Manager

from whuhole.app import create_app

app = create_app()
manager = Manager(app)


@manager.command
def runserver(port=3000):
    from flask import send_from_directory
    from gevent.wsgi import WSGIServer
    from werkzeug.serving import run_with_reloader
    from werkzeug.debug import DebuggedApplication

    port = int(port)

    @app.route('/static/<path:filename>')
    def static_file(filename):
        datadir = os.path.abspath('assets/static')
        return send_from_directory(datadir, filename)

    wsgi = DebuggedApplication(app)

    @run_with_reloader
    def run_server():
        print('Start server at: 127.0.0.1:%d' % port)

        http_server = WSGIServer(('', port), wsgi)
        http_server.serve_forever()

    try:
        run_server()
    except KeyboardInterrupt:
        sys.exit(0)


@manager.command
def syncdb():
    from whuhole.models import db
    db.create_all()


if __name__ == '__main__':
    manager.run()
