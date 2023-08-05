#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='piptest_0922',
    version='1.0.0',
    description='Dummy',
    long_description="description",
    url='https://github.com/Nobu19800/piptest',
    author='nobu',
    author_email='nobu@nobu777.net',
    license='MIT',
    install_requires=[],
    keywords='dummy',
    packages=find_packages(exclude=('tests')),
    entry_points={
        "console_scripts": [
            "piptest=piptest.__init__:main",
        ],
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.7',
    ],
)