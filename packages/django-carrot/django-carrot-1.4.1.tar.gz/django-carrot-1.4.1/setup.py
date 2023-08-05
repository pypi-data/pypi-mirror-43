# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['carrot',
 'carrot.management',
 'carrot.management.commands',
 'carrot.migrations']

package_data = \
{'': ['*'], 'carrot': ['static/carrot/*', 'templates/carrot/*']}

install_requires = \
['django>=2.1,<3.0',
 'djangorestframework>=3.9,<4.0',
 'json2html>=1.2,<2.0',
 'pika>=0.13.1,<0.14.0',
 'psutil>=5.6,<6.0',
 'sphinx_bootstrap_theme>=0.6.5,<0.7.0']

setup_kwargs = {
    'name': 'django-carrot',
    'version': '1.4.1',
    'description': 'A RabbitMQ asynchronous task queue for Django.',
    'long_description': None,
    'author': 'Christoper Davies',
    'author_email': 'christopherdavies553@gmail.com',
    'url': 'https://django-carrot.readthedocs.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.3,<4.0.0',
}


setup(**setup_kwargs)
