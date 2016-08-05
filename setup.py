#!/usr/bin/env python

from distutils.core import setup

setup(
    name='Reconbot',
    version='1.0',
    license='MIT License',
    description='Reconbot for Eve Online',
    packages=[
        'reconbot',
        'reconbot.notifiers'
    ]
)
