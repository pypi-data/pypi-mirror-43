# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dtc']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dtc',
    'version': '0.1.1',
    'description': 'Generate Dataclass without writting them !',
    'long_description': '.. image:: https://travis-ci.org/jgirardet/dtc.svg?branch=master\n    :target: https://travis-ci.org/jgirardet/dtc\n\n.. image:: https://ci.appveyor.com/api/projects/status/ffd44ndqx713yuhd/branch/master?svg=true\n    :target: https://ci.appveyor.com/project/jgirardet/dtc\n\n=======================================================\nDTC :"Generate Dataclasses without writting them !"\n=======================================================\n\n\n.. warning::\n\t\t\n\tThis is an alpha version\n\n\nBasic Usage\n------------\n\n.. code-block:: python\n\t\t\n\t    >>> import dtc\n\n\t    >>> JSON = b"""{"flooat": 12.564, "boolean": true, "integer": 12}"""\n\n\t    >>> my_class = dtc.from_json(JSON)\n\n\t    >>> my_class\n\t    Base(flooat=12.564, boolean=True, integer=12)\n\n\t    >>> from dataclasses import *\n\t    >>> is_dataclass(my_class)\n\t    True\n\n\t    >>> JSON = b"""[{"flooat": 12.4, "boolean": true, "integer": 1}, {"flooat": 12.564, "boolean": true, "integer": 12},{"flooat": 1.4, "boolean": false, "integer": 0}]"""\n\t    >>> dtc.from_json(JSON\n\t\t[Base(flooat=12.4, boolean=True, integer=1), Base(flooat=12.564, boolean=True, integer=12), Base(flooat=1.4, boolean=False, integer=0)]\n\n\t\n\n\n* License : GNU General Public License v3 or later (GPLv3+) \n* Source: https://github.com/jgirardet/dtc\n\n\n',
    'author': 'jgirardet',
    'author_email': 'ijkl@netc.fr',
    'url': 'https://github.com/jgirardet/dtc',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
