# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['flask_dramatiq']
setup_kwargs = {
    'name': 'flask-dramatiq',
    'version': '0.1.0',
    'description': 'Adds Dramatiq support to your Flask application',
    'long_description': None,
    'author': 'Étienne BERSAC',
    'author_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
