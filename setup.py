#!/usr/bin/env python

from setuptools import setup

def readme():
    try: # 3.x
        with open('README.md', 'r', encoding="utf8") as f:
            return f.read()
    except:
        with open('README.md', 'r') as f:
            return f.read()

setup(name='match',
      version='0.1',
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
      packages=['match'])
