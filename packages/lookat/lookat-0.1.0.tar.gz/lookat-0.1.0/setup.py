# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['lookat']
setup_kwargs = {
    'name': 'lookat',
    'version': '0.1.0',
    'description': 'Explore variables during debug',
    'long_description': None,
    'author': 'Antoine Gallix',
    'author_email': 'antoine.gallix@gmail.com',
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
