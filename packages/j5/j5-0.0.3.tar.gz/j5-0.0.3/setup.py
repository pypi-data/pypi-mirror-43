# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['j5',
 'j5.backends',
 'j5.backends.dummy',
 'j5.backends.hardware',
 'j5.backends.hardware.sr',
 'j5.backends.hardware.sr.v4',
 'j5.boards',
 'j5.boards.j5',
 'j5.boards.sr',
 'j5.boards.sr.v4',
 'j5.components']

package_data = \
{'': ['*']}

install_requires = \
['pyusb>=1.0,<2.0']

setup_kwargs = {
    'name': 'j5',
    'version': '0.0.3',
    'description': 'J5 Robotics API',
    'long_description': None,
    'author': 'j5 contributors',
    'author_email': 'sro@soton.ac.uk',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
