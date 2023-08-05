# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['flask_dramatiq']
install_requires = \
['dramatiq>=1.5,<2.0', 'flask-migrate>=2.4,<3.0']

entry_points = \
{'flask.commands': ['worker = flask_dramatiq:worker']}

setup_kwargs = {
    'name': 'flask-dramatiq',
    'version': '0.2.0',
    'description': 'Adds Dramatiq support to your Flask application',
    'long_description': '# // Flask-Dramatiq //\n\nFlask-Dramatiq plugs [Dramatiq](https://dramatiq.io) in your\n[Flask](https://flask.pocoo.org) application.\n\n## Features\n\n- Configure Dramatiq from Flask configuration.\n- Ensure Flask app is available to Dramatiq actor.\n- Add `worker` command to Flask CLI.\n- Enable [Flask Application factory](http://flask.pocoo.org/docs/dev/tutorial/factory/).\n\n\n## Installation and Usage\n\nFlask-Dramatiq is licensed under BSD-3-Clause. Add `flask-dramatiq` to your\nproject:\n\n``` console\n$ poetry add flask-dramatiq\n```\n\nThen use `Dramatiq` object as a regular Flask extension:\n\n``` python\nfrom flask import Flask\nfrom flask_dramatiq import Dramatiq\n\napp = Flask(__name__)\ndramatiq = Dramatiq(app)\n\n@dramatiq.actor()\ndef my_actor():\n    ...\n\n@app.route("/")\ndef myhandler():\n    my_actor.send()\n```\n\nNow run worker program to consume messages and execute tasks in the background:\n\n``` console\n$ flask worker --processes=1\n```\n\nA complete flask app is available in project source tree\n[example.py](https://gitlab.com/bersace/flask-dramatiq/blob/master/example.py).\n\n\n## Credit and Support\n\nFeel free to open an issue or suggest a merge request on [Gitlab project\npage](https://gitlab.com/bersace/flask-dramatiq). Contribution welcome!\n\nThe project is based on\n[Bogdanp/flask_dramatiq_example](https://github.com/Bogdanp/flask_dramatiq_example).\n',
    'author': 'Étienne BERSAC',
    'author_email': None,
    'url': 'https://pypi.org/project/flask-dramatiq',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
