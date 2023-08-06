# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['siphono_notify']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.21,<3.0']

setup_kwargs = {
    'name': 'siphono-notify',
    'version': '0.1.0',
    'description': 'Module for sending notifications through siphono notify.',
    'long_description': None,
    'author': 'Kevin Schiroo',
    'author_email': 'kjschiroo@siphono.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
