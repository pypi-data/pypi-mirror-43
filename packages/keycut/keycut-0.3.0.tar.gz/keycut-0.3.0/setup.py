# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['keycut']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=3.13,<4.0', 'termcolor>=1.1,<2.0']

entry_points = \
{'console_scripts': ['keycut = keycut.cli:main']}

setup_kwargs = {
    'name': 'keycut',
    'version': '0.3.0',
    'description': 'A command line tool that helps you remembering ALL the numerous keyboard shortcuts of ALL your favorite programs.',
    'long_description': '<!--\nIMPORTANT:\n  This file is generated from the template at \'scripts/templates/README.md\'.\n  Please update the template instead of this file.\n-->\n\n# keycut\n![logo](logo.jpg)\n\n[![pipeline status](https://github.com/pawamoy/keycut/badges/master/pipeline.svg)](https://github.com/pawamoy/keycut/commits/master)\n[![coverage report](https://github.com/pawamoy/keycut/badges/master/coverage.svg)](https://github.com/pawamoy/keycut/commits/master)\n[![documentation](https://img.shields.io/readthedocs/keycut.svg?style=flat)](https://keycut.readthedocs.io/en/latest/index.html)\n[![pypi version](https://img.shields.io/pypi/v/keycut.svg)](https://pypi.org/project/keycut/)\n\nA command line tool that helps you remembering ALL the numerous keyboard shortcuts of ALL your favorite programs.\n\nKeyCut (for keyboard shortcut) is a command line tool\nthat helps you remembering the numerous keyboard shortcuts\nof your favorite programs, both graphical and command line ones,\nby allowing you to print them quickly in a console and search through them.\n\nShortcut data are provided by the [keycut-data][1].\n\nThis repository contains the sources for a Python implementation of KeyCut.\n\n[keycut-data]: https://github.com/pawamoy/keycut-data\n\n## How it looks\n\nThe yellow parts are the one that matched a pattern using a regular expression.\n\n![screenshot](http://i.imgur.com/ZaqTOUb.png)\n\n## Requirements\nkeycut requires Python 3.6 or above.\n\n<details>\n<summary>To install Python 3.6, I recommend using <a href="https://github.com/pyenv/pyenv"><code>pyenv</code></a>.</summary>\n\n```bash\n# install pyenv\ngit clone https://github.com/pyenv/pyenv ~/.pyenv\n\n# setup pyenv (you should also put these three lines in .bashrc or similar)\nexport PATH="${HOME}/.pyenv/bin:${PATH}"\nexport PYENV_ROOT="${HOME}/.pyenv"\neval "$(pyenv init -)"\n\n# install Python 3.6\npyenv install 3.6.8\n\n# make it available globally\npyenv global system 3.6.8\n```\n</details>\n\n## Installation\nWith `pip`:\n```bash\npython3.6 -m pip install keycut\n```\n\nWith [`pipx`](https://github.com/cs01/pipx):\n```bash\n# install pipx with the recommended method\ncurl https://raw.githubusercontent.com/cs01/pipx/master/get-pipx.py | python3\n\npipx install --python python3.6 keycut\n```\n\nYou will also need to download the data by cloning the repository somewhere:\n\n```\ngit clone https://github.com/pawamoy/keycut-data ~/.keycut-data\n```\n\n## Usage\nThe program needs to know where the data are. By default, it will search\nin the (relative) `keycut-data/default` directory.\n\n```\nexport KEYCUT_DATA=~/.keycut-data/default\n```\n\nShow all bash shortcuts:\n\n```\nkeycut bash\n```\n\nShow all bash shortcuts matching *proc* (in Category, Action, or Keys):\n\n```\nkeycut bash proc\n```\n\nCommand-line help:\n\n```\nusage: keycut [-h] APP [PATTERN]\n\nCommand description.\n\npositional arguments:\n  APP         The app to print shortcuts of.\n  PATTERN     A regex pattern to search for.\n\noptional arguments:\n  -h, --help  show this help message and exit\n\n```\n\n\n',
    'author': 'Timothée Mazzucotelli',
    'author_email': 'pawamoy@pm.me',
    'url': 'https://github.com/pawamoy/keycut',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
