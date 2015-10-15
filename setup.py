#!/usr/bin/env python

import io
from setuptools import setup

def readme():
    with io.open('README.txt', 'r', encoding="utf8") as f:
        return f.read()

setup(name='match',
      version='0.2.2',
      description=(''),
      long_description=readme(),
      keywords='tokenization',
      url='https://github.com/EducationalTestingService/match',
      author='Diane Napolitano',
      author_email='dnapolitano@ets.org',
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Topic :: Text Processing",
      ],
      packages=['match'],
      install_requires=[
        "python>=2.7",
        "nltk",
        "regex"])
