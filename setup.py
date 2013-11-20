#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from setuptools import setup, find_packages
import setuptools

setup(
    name='prismic',
    version='0.1.2',
    description='Prismic.io development kit',
    author='Nicolae Namolovan',
    author_email='nna@zenexity.com',
    url='http://prismic.io',
    license='Apache 2',
    packages=find_packages(),
    test_suite='tests',
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7'
    ]
)
