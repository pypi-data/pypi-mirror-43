# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['mailgun_cli']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.1.3,<0.2.0', 'uplink>=0.8.0,<0.9.0']

entry_points = \
{'console_scripts': ['mailgun = mailgun-cli:console.run']}

setup_kwargs = {
    'name': 'mailgun-cli',
    'version': '0.1.2',
    'description': 'mailgun cli, forwarding mail',
    'long_description': None,
    'author': 'Nutchanon Ninyawee ',
    'author_email': 'dev@nutchanon.org',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
