# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['advanced_plot']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.0,<4.0', 'seaborn>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'advanced-plot',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Ikeda Yutao',
    'author_email': 'yutaro.ikeda@kaizenplatform.com',
    'url': 'https://github.com/ikedaosushi/advanced-plot',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
