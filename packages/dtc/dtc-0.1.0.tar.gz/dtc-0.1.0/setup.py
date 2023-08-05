# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dtc']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dtc',
    'version': '0.1.0',
    'description': 'Generate Dataclass without writting them !',
    'long_description': None,
    'author': 'jgirardet',
    'author_email': 'ijkl@netc.fr',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
