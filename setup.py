#!/usr/bin/env python

from distutils.core import setup
from dotenv import load_dotenv
load_dotenv()

setup(
    name='Reconbot',
    version='1.0',
    license='MIT License',
    description='Reconbot for Eve Online',
    packages=[
        'reconbot',
        'reconbot.notifiers',
        'reconbot.notificationprinters',
    ]
)