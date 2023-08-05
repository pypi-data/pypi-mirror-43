#!/usr/bin/env python

import sys
from setuptools import setup

setup(
    name='werkzeug-encryptedcookie',
    version='2.0',
    url='https://github.com/homm/werkzeug-encryptedcookie',
    author='Alexander Karpinsky',
    author_email='homm86@gmail.com',
    description='Werkzeug encrypted cookie',
    packages=['werkzeug_encryptedcookie'],
    platforms='any',
    install_requires=['PyCrypto>=2.5', 'werkzeug', 'six'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    test_suite='test',
)
