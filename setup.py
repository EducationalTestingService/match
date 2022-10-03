#!/usr/bin/env python

from setuptools import setup


def readme():
    with open('README.rst', 'r', encoding='utf-8') as f:
        return f.read()


def requirements():
    with open('requirements.txt', 'r') as fh:
        return [line.strip() for line in fh]


setup(name='match',
      version='0.3.2',
      description=('Match tokenized words and phrases within the original, untokenized, often messy, text.'),
      long_description=readme(),
      keywords='tokenization',
      url='https://github.com/EducationalTestingService/match',
      author='Diane Napolitano',
      author_email='dmnapolitano@gmail.com',
      maintainer='Tamar Lavee',
      maintainer_email='tlavee@ets.org',
      classifiers=[
          'License :: OSI Approved :: Apache Software License',
          'Topic :: Text Processing',
          'Programming Language :: Python',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Operating System :: Unix',
          'Operating System :: MacOS',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
      ],
      packages=['match'],
      install_requires=requirements()
      )
