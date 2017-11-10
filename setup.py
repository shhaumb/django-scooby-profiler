#!/usr/bin/env python

from setuptools import setup

# setup the project
setup(
    name="scooby-django",
    version="0.0.1",
    author="HackerEarth",
    author_email="support@hackerearth.com",
    description="Scooby",
    license="MIT",
    packages=[
        'scooby',
    ],
    install_requires=[
        'redis==2.10.6',
    ]
)
