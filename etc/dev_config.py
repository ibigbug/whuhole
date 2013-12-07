import os
rootdir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
database = os.path.join(rootdir, 'data', 'development.sqlite')

DEBUG = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % database
