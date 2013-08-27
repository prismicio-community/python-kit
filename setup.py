#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from setuptools import setup, find_packages
import setuptools

setup(
    name='Prismic',
    version='0.1',
    description='Prismic.io kit',
    packages=find_packages(),
    test_suite="tests",
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7'
    ]
)
