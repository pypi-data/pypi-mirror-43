# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['mattes_dada', 'mattes_dada.model', 'mattes_dada.nltk_data', 'mattes_dada.odt']

package_data = \
{'': ['*']}

install_requires = \
['markovify>=0.7.1,<0.8.0', 'nltk>=3.4,<4.0', 'regex>=2019.2,<2020.0']

entry_points = \
{'console_scripts': ['mdada = mattes_dada.cmd:main']}

setup_kwargs = {
    'name': 'mattes-dada',
    'version': '0.2.2',
    'description': 'Semi-random text generator using Markov chains',
    'long_description': "Matte's Dada\n===\n\nSemi-random text generator using Markov chains\n\n[![Build Status](https://travis-ci.org/mattesilver/dada.svg?branch=master)](https://travis-ci.org/mattesilver/dada)\n![PyPI](https://img.shields.io/pypi/v/mattes-dada.svg?style=plastic)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mattes-dada.svg?style=plastic)\n[![codecov](https://codecov.io/gh/mattesilver/dada/branch/master/graph/badge.svg)](https://codecov.io/gh/mattesilver/dada)\n\nUsage\n==\n\n```shell\nmdada input_file\n```\n\nwhere input_file is a path to either a txt ot odt file.\n\nExample output:\n\n```\nthe emancipation proclamation, the phrase goes, thirty, when, as the principal insurgent army, could not whether they ask the white, the new louisiana\nnow, and means of constituency, reached, and yet been my duty to some supposed to my own opinion whether these, the arms of louisiana, a national constitution, whenever i shall treat with it\nif we, as before stated\nwe say this i abstain from any professed emancipationist, adopted a new state, and each state government for him, civil and inflexible plan\ni shall sooner by sustaining it\n```",
    'author': 'Raphael Krupinski',
    'author_email': None,
    'url': 'https://github.com/mattesilver/dada',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
