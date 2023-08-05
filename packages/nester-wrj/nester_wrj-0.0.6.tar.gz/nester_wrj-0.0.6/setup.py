#!/usr/bin/env python
# encoding: utf-8
'''
@author: baige
@license: (C) Copyright 2018
@contact: jeckerWen@gmail.com
@file: setup.py
@Date: 2019/3/1 9:55
@desc:
'''

import setuptools

with open('README.md', 'r', encoding='utf-8') as  fh:
    long_description = fh.read()

setuptools.setup(
    name = 'nester_wrj',
    version = '0.0.6',
    author = 'WenRj',
    author_email = 'jeckerWen@gmail.com',
    url = 'https://github.com/JeckerWen',
    description = 'lalal!',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    packages = setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
