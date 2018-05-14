#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='xblog',
    version='0.0',
    author='Dongjie Chen',
    author_email='midwinter1993@gmail.com',
    packages=['xblog', 'xblog.misc', 'xblog.theme'],
    package_data={'xblog.theme': ['*', '*/*']},
    include_package_data=True,
    scripts=['xblog/xblog'],
    url='http://github.com/midwinter1993/8blog',
    license='LICENSE',
    description='My simple blog generator.',
    long_description=open('README.md').read(),
    install_requires=open('requirements.txt').read().strip().split('\n')
)
