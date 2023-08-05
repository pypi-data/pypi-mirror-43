# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['poetry_org']

package_data = \
{'': ['*']}

install_requires = \
['toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['poetry-org = poetry_org:main']}

setup_kwargs = {
    'name': 'poetry-org',
    'version': '0.1.0',
    'description': 'Re-organize a single-file app into a poetry directory for building.',
    'long_description': None,
    'author': 'Manny Ochoa',
    'author_email': 'dev@manuelochoa.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
