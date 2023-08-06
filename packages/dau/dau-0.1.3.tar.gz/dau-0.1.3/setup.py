# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dau']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.1,<3.0']

setup_kwargs = {
    'name': 'dau',
    'version': '0.1.3',
    'description': 'Automatic user creation at Django startup.',
    'long_description': "\n[![Build Status](https://travis-ci.org/AndreGuerra123/django_autouser.png)](https://travis-ci.org/AndreGuerra123/django_autouser)\n[![codecov](https://codecov.io/gh/AndreGuerra123/django_autouser/branch/master/graph/badge.svg)](https://codecov.io/gh/AndreGuerra123/django_autouser)\n\n# Django Auto User\n\nDjango Auto User (DAU) is a Django (Python) library for the automatic creation of users.\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install Django Auto User.\n\n```bash\n\npip install dau\n\n```\n\n## Usage\n\nAdd 'dau' to INSTALLED APPS after 'django.contrib.admin' in your settings.py:\n\n\n```python\n\nINSTALLED_APPS = [\n    ...\n    'django.contrib.admin',\n    'dau',\n    ...\n]\n\n```\n\nThen, just add DJANGO_AUTO_USER settings to your settings.py file as:\n\n```python\n\nDJANGO_AUTO_USER = [\n    {\n        'username':'admin',\n        'email':'admin@admin.com',\n        'password':'adminpass',\n        'is_superuser':True,\n        'is_staff':True,\n        'is_active':True\n    }\n]\n\n```\n\nMake your migrations with:\n\n```bash\n\npython manage.py makemigrations\npython manage.py migrate\n\n```\n\n\n## Contributing\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\nPlease make sure to update tests as appropriate.\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)\n",
    'author': 'AndreGuerra123',
    'author_email': 'guerraandre@hotmail.com',
    'url': 'https://github.com/AndreGuerra123/dau',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
