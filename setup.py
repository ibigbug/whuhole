from setuptools import setup, find_packages
from email.utils import parseaddr
from babel.messages import frontend as babel

import whuhole

author, author_email = parseaddr(whuhole.__author__)

setup(
    name='whuhole',
    version=whuhole.__version__,
    author=author,
    author_email=author_email,
    url='example.com',
    packages=find_packages(),
    license='BSD',
    zip_safe=False,
    include_package_data=True,

    install_requires=[
        'Flask',
        'False-SQLAlchemy',
        'Flask-Cache',
        'Flask-Babel',
        'Flask-WTF',
        'Flask-Script',

        'gevent'
    ],
    cmdclass = {
        'compile_catalog': babel.compile_catalog,
        'extract_messages': babel.extract_messages,
        'init_catalog': babel.init_catalog,
        'update_catalog': babel.update_catalog
    },

    message_extractors = {
        'whuhole': [
            ('whuhole/**.py', 'python', None),
            ('whuhole/templates/**.html', 'jinja2', {
                'extensions': (
                    'jinja2.ext.autoescape',
                    'jinja2.ext.with_'
                )
            })
        ]
    }
)
