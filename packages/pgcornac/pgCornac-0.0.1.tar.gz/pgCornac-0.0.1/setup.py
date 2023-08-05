# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['cornac',
 'cornac.core',
 'cornac.core.schema',
 'cornac.iaas',
 'cornac.operator']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'flask-sqlalchemy>=2.3,<3.0',
 'flask>=1.0,<2.0',
 'tenacity>=5.0,<6.0']

entry_points = \
{'console_scripts': ['cornac = cornac.cli:entrypoint']}

setup_kwargs = {
    'name': 'pgcornac',
    'version': '0.0.1',
    'description': 'RDS-compatible Managed-Postgres Webservice',
    'long_description': None,
    'author': 'Étienne BERSAC',
    'author_email': 'etienne.bersac@dalibo.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
