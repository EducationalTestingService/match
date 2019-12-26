#!/usr/bin/env python

from setuptools import setup


def readme():
    with open('README.txt', 'r') as f:
        return f.read()


def requirements():
    with open('requirements.txt', 'r') as fh:
        return [line.strip() for line in fh]


setup(name='match',
      version='0.3.0',
      description=(''),
      long_description=readme(),
      keywords='tokenization',
      url='https://github.com/EducationalTestingService/match',
      author='Diane Napolitano',
      author_email='dmnapolitano@gmail.com',
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Topic :: Text Processing",
      ],
      packages=['match'],
      install_requires=requirements()
      )
