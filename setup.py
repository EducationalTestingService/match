#!/usr/bin/env python

from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='match',
      version='0.1',
      description=(''),
      long_description=readme(),
      keywords='tokenization',
      url='https://github.com/EducationalTestingService/match'
      author='Diane Napolitano',
      author_email='dnapolitano@ets.org',
      license='GPLv2',
      packages=['match'])
