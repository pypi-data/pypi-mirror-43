# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['artworks']
install_requires = \
['mutagen>=1.42,<2.0']

setup_kwargs = {
    'name': 'artworks',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'castaneai',
    'author_email': 'castaneai@castaneai.net',
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
