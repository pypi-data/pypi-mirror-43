#!/usr/bin/env python
# vim: set sw=4 et:

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import glob

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)

    def run_tests(self):
        import pytest
        import sys
        import os
        errcode = pytest.main(['--doctest-module', './wsgiprox', '--cov', 'wsgiprox', '-v', 'test/'])
        sys.exit(errcode)


setup(
    name='wsgiprox',
    version='1.5.2',
    author='Ilya Kreymer',
    author_email='ikreymer@gmail.com',
    license='Apache 2.0',
    packages=find_packages(),
    url='https://github.com/webrecorder/wsgiprox',
    description='HTTP/S proxy with WebSockets over WSGI',
    long_description=open('README.rst').read(),
    provides=[
        'wsgiprox'
        ],
    install_requires=[
        'six',
        'certauth>=1.2.1',
        ],
    zip_safe=True,
    data_files=[
    ],
    extras_require={
        'gevent-websocket':  ['gevent-websocket'],
    },
    entry_points="""
        [console_scripts]
    """,
    cmdclass={'test': PyTest},
    test_suite='',
    tests_require=[
        'mock',
        'pytest',
        'pytest-cov',
        'gevent',
        'requests',
        'websocket-client',
        'waitress',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ]
)
