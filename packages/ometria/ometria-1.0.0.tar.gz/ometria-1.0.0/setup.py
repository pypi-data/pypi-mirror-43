#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='ometria',
    version='1.0.0',
    description='Python wrapper for the Ometria API',
    long_description=readme + '\n\n' + history,
    author='Neil Lyons',
    author_email='nwjlyons@googlemail.com',
    url='https://github.com/nwjlyons/ometria',
    packages=[
        'ometria',
    ],
    package_dir={'ometria': 'ometria'},
    include_package_data=True,
    install_requires=[
        'requests',
    ],
    license="BSD",
    zip_safe=False,
    keywords='ometria',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=[
        'httpretty',
    ]
)
