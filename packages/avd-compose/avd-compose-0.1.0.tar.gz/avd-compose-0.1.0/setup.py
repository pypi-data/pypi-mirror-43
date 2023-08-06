# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['avd_compose']

package_data = \
{'': ['*'], 'avd_compose': ['androidstudio/*', 'utils/*']}

install_requires = \
['PyYAML>=3.13,<4.0', 'click>=7.0,<8.0', 'delegator.py>=0.1.1,<0.2.0']

entry_points = \
{'console_scripts': ['avd-compose = avd_compose.cli:main']}

setup_kwargs = {
    'name': 'avd-compose',
    'version': '0.1.0',
    'description': 'Define and run android virtual devices',
    'long_description': '# avd-compose [![PyPi version](https://img.shields.io/pypi/v/avd-compose.svg)](https://pypi.python.org/pypi/avd-compose/) [![PyPI pyversions](https://img.shields.io/pypi/pyversions/avd-compose.svg)](https://pypi.python.org/pypi/avd-compose/) [![](https://img.shields.io/github/license/f9n/avd-compose.svg)](https://github.com/f9n/avd-compose/blob/master/LICENSE)\n\nDefine and run android virtual devices\n\n## Install\n\n```bash\n$ pip3 install --user avd-compose\n```\n\n# Examples\n\nLook up the [examples](https://github.com/f9n/avd-compose/tree/master/examples) directory.\n\n# Credits\n\n- [Docker Compose](https://github.com/docker/compose)\n- [Vagrant](https://github.com/hashicorp/vagrant)\n',
    'author': 'Fatih Sarhan',
    'author_email': 'f9n@protonmail.com',
    'url': 'https://github.com/f9n/avd-compose',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
