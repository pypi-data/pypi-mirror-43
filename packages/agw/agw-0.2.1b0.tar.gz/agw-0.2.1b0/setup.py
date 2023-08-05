# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['agw']

package_data = \
{'': ['*']}

install_requires = \
['cutie>=0.2.2,<0.3.0', 'pyautogui>=0.9.41,<0.10.0']

extras_require = \
{':sys_platform == "darwin"': ['pyobjc-core>=5.1,<6.0',
                               'pyobjc-framework-Quartz>=5.1,<6.0']}

setup_kwargs = {
    'name': 'agw',
    'version': '0.2.1b0',
    'description': 'A pyautogui wrapper library for data entry macros.',
    'long_description': None,
    'author': 'Mark Gemmill',
    'author_email': 'contact@markgemmill.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
