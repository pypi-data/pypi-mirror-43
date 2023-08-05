# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['fileexpect']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fileexpect',
    'version': '1.0.0',
    'description': 'Tool to compare test results against file content',
    'long_description': None,
    'author': 'François Trahan',
    'author_email': 'francois.trahan@gmail.com',
    'url': 'https://github.com/francoistrahan/fileexpect',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
