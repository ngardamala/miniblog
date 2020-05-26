#!/usr/bin/env python
import os
from flask_script import Manager, Command, Option

from app import create_app

gunicorn_host = os.environ.get('GUNICORN_HOST') or '127.0.0.1'
gunicorn_port = os.environ.get('GUNICORN_PORT') or 8000
gunicorn_workers = os.environ.get('GUNICORN_WORKERS') or 4


class GunicornServer(Command):

    description = 'Run the app within Gunicorn'

    def __init__(self, host='127.0.0.1', port=8000, workers=4):
        self.port = port
        self.host = host
        self.workers = workers

    def get_options(self):
        return (
            Option('-H', '--host',
                   dest='host',
                   default=self.host),

            Option('-p', '--port',
                   dest='port',
                   type=int,
                   default=self.port),

            Option('-w', '--workers',
                   dest='workers',
                   type=int,
                   default=self.workers),
        )

    def __call__(self, app, host, port, workers):

        from gunicorn import version_info

        if version_info < (0, 9, 0):
            from gunicorn.arbiter import Arbiter
            from gunicorn.config import Config
            arbiter = Arbiter(Config({'bind': "%s:%d" % (host, int(port)),
                                     'workers': workers}), app)
            arbiter.run()
        else:
            from gunicorn.app.base import Application

            class FlaskApplication(Application):
                def init(self, parser, opts, args):
                    return {
                        'bind': '{0}:{1}'.format(host, port),
                        'workers': workers
                    }

                def load(self):
                    return app

            FlaskApplication().run()


app = create_app()
app.config.from_object(os.environ['APP_SETTINGS'])
manager = Manager(app)
manager.add_command("gunicorn", GunicornServer(host=gunicorn_host,
                                               port=gunicorn_port,
                                               workers=gunicorn_workers))


if __name__ == '__main__':
    manager.run()
