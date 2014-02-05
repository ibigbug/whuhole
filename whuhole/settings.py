import os
proj_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
db_path = os.path.join(proj_dir, 'whuhole.sqlite')

DEBUG = True
SECRET_KEY = 'secret key'
SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % db_path

SITE_TITLE = 'WHU Hole'
