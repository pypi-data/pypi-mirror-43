#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup script for Munchkin API
"""

import sys

from setuptools import setup, find_packages

NAME = "munchkinapi"
VERSION = "0.0.1"
DESCRIPTION = "Munckin server side API"
AUTHOR = "EH-PI Team"
AUTHOR_EMAIL = "thomas.huba@etu.unistra.fr"
LICENSE = "GNU/GPL"
# TODO: Change this url to presentation website when it's available
URL = "https://git.unistra.fr/huba/eh-pi/tree/develop/packages/api"

if sys.version_info[:2] < (3, 5):
    print("MunckinAPI requires Python 3.5 or later (%d.%d detected)." %
          sys.version_info[:2])
    sys.exit(-1)

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    packages=find_packages(exclude=["test"]),
    license=LICENSE,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ],
    install_requires=[
        "cerberus==1.2",
        "tornado==5.1.1"
    ]
)
