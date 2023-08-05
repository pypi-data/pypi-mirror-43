# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['ansito']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['ansito = ansito.cli:main']}

setup_kwargs = {
    'name': 'ansito',
    'version': '0.1.0',
    'description': 'Translate ANSI codes to any other format.',
    'long_description': '<!--\nIMPORTANT:\n  This file is generated from the template at \'scripts/templates/README.md\'.\n  Please update the template instead of this file.\n-->\n\n# ansito\n[![pipeline status](https://gitlab.com/pawamoy/ansito/badges/master/pipeline.svg)](https://gitlab.com/pawamoy/ansito/pipelines)\n[![coverage report](https://gitlab.com/pawamoy/ansito/badges/master/coverage.svg)](https://gitlab.com/pawamoy/ansito/commits/master)\n[![documentation](https://img.shields.io/readthedocs/ansito.svg?style=flat)](https://ansito.readthedocs.io/en/latest/index.html)\n[![pypi version](https://img.shields.io/pypi/v/ansito.svg)](https://pypi.org/project/ansito/)\n\nTranslate ANSI codes to any other format.\n\nCurrently, only Conky format is supported.\n\n## Requirements\nansito requires Python 3.6 or above.\n\n<details>\n<summary>To install Python 3.6, I recommend using <a href="https://github.com/pyenv/pyenv"><code>pyenv</code></a>.</summary>\n\n```bash\n# install pyenv\ngit clone https://github.com/pyenv/pyenv ~/.pyenv\n\n# setup pyenv (you should also put these three lines in .bashrc or similar)\nexport PATH="${HOME}/.pyenv/bin:${PATH}"\nexport PYENV_ROOT="${HOME}/.pyenv"\neval "$(pyenv init -)"\n\n# install Python 3.6\npyenv install 3.6.8\n\n# make it available globally\npyenv global system 3.6.8\n```\n</details>\n\n## Installation\nWith `pip`:\n```bash\npython3.6 -m pip install ansito\n```\n\nWith [`pipx`](https://github.com/cs01/pipx):\n```bash\n# install pipx with the recommended method\ncurl https://raw.githubusercontent.com/cs01/pipx/master/get-pipx.py | python3\n\npipx install --python python3.6 ansito\n```\n\n## Usage (as a library)\nTODO\n\n## Usage (command-line)\n```\nusage: ansito [-h] FILENAME\n\npositional arguments:\n  FILENAME    File to translate, or - for stdin.\n\noptional arguments:\n  -h, --help  show this help message and exit\n\n```\n\nExample:\n\n```bash\ncommand-that-output-colors | ansito -\n```\n\nReal-word example with `taskwarrior` in a Conky configuration file:\n\n```lua\n${texecpi 60 flock ~/.task task limit:10 rc.defaultwidth:80 rc._forcecolor:on rc.verbose:affected,blank list | ansito - | sed -r \'s/([^ ])#/\\1\\\\#/g\'\n```\n\n\n',
    'author': 'Timothée Mazzucotelli',
    'author_email': 'pawamoy@pm.me',
    'url': 'https://github.com/pawamoy/ansito',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
