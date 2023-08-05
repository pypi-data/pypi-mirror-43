# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['bouchon']

package_data = \
{'': ['*']}

install_requires = \
['flask>=1.0,<2.0', 'gunicorn>=19.9,<20.0']

setup_kwargs = {
    'name': 'bouchon',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Romain Dorgueil',
    'author_email': 'romain@dorgueil.net',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
