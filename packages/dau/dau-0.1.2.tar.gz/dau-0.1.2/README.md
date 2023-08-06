
[![Build Status](https://travis-ci.org/AndreGuerra123/django_autouser.png)](https://travis-ci.org/AndreGuerra123/django_autouser)
[![codecov](https://codecov.io/gh/AndreGuerra123/django_autouser/branch/master/graph/badge.svg)](https://codecov.io/gh/AndreGuerra123/django_autouser)

# Django Auto User

Django Auto User (DAU) is a Django (Python) library for the automatic creation of users.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Django Barcode.

```bash

pip install dau

```

## Usage

Add 'dau' to INSTALLED APPS after 'django.contrib.admin' in your settings.py:


```python

INSTALLED_APPS = [
    ...
    'django.contrib.admin',
    'dau',
    ...
]

```

Then, just add DJANGO_AUTO_USER settings to your settings.py file as:

```python

DJANGO_AUTO_USER = [
    {
        'username':'admin',
        'email':'admin@admin.com',
        'password':'adminpass',
        'is_superuser':True,
        'is_staff':True,
        'is_active':True
    }
]

```

Make your migrations with:

```bash

python manage.py makemigrations
python manage.py migrate

```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
