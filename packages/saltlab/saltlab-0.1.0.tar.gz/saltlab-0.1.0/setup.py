# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['saltlab']

package_data = \
{'': ['*']}

install_requires = \
['camel>=0.1.2,<0.2.0',
 'click>=7.0,<8.0',
 'docker>=3.7,<4.0',
 'setuptools>=40.8,<41.0']

entry_points = \
{'console_scripts': ['saltlab = saltlab.cli:saltlab']}

setup_kwargs = {
    'name': 'saltlab',
    'version': '0.1.0',
    'description': 'SaltStack experimental setup manager',
    'long_description': None,
    'author': 'Jamie Bliss',
    'author_email': 'jamie@ivyleav.es',
    'url': 'https://gitlab.com/spirostack/saltlab',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
