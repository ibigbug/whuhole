import os
import tempfile
from whuhole.app import create_app
from whuhole.models import db


class BaseSuite(object):
    def setUp(self):
        config = {'TESTING': True}
