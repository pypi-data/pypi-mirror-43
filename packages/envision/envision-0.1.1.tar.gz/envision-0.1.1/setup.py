# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['envision', 'envision.tests']

package_data = \
{'': ['*'],
 'envision.tests': ['dev_warnings/*',
                    'git_warnings/*',
                    'invalid_envision_file/*',
                    'invalid_envision_key_value/*',
                    'invalid_envision_lock_file/*',
                    'invalid_envision_lock_key_value/*',
                    'prod_warnings/*',
                    'valid_dev/*',
                    'valid_prod/*']}

install_requires = \
['click>=7.0,<8.0', 'cryptography>=2.6,<3.0']

entry_points = \
{'console_scripts': ['envision = envision:cli']}

setup_kwargs = {
    'name': 'envision',
    'version': '0.1.1',
    'description': 'A encrypted environment variables manager for python projects',
    'long_description': None,
    'author': 'AndreGuerra123',
    'author_email': 'guerraandre@hotmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
