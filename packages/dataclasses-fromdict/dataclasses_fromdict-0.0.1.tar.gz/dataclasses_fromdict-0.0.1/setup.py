#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = ''

long_description = None

if os.path.isfile('README.md'):
    with open('README.md') as f:
        long_description = f.read()

long_description = long_description or DESCRIPTION

setup(
    name = 'dataclasses_fromdict',
    version = VERSION,
    description = DESCRIPTION,
    long_description = long_description or DESCRIPTION,
    long_description_content_type="text/markdown",
    classifiers = [],
    keywords = ['python', 'dataclass', 'fromdict'],
    author = 'cologler',
    author_email='skyoflw@gmail.com',
    url = 'https://github.com/Cologler/dataclasses_fromdict-python',
    license = 'MIT',
    packages = find_packages(),
    include_package_data = True,
    install_requires = [],
    zip_safe = False,
    entry_points = {}
)