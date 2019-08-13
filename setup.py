#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from setuptools import setup, find_packages
import setuptools

setup(
    name='prismic',
    version='1.5.1',
    description='Prismic.io development kit',
    author='The Prismic.io Team',
    author_email='contact@prismic.io',
    url='http://prismic.io',
    license='Apache 2',
    packages=find_packages(),
    test_suite='tests',
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7'
    ],
    install_requires=[
        'pyOpenSSL',
        'ndg-httpsclient',
        'pyasn1',
        'requests >= 2.7'
    ]
)
