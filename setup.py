#!/usr/bin/env python

import os
from setuptools import setup, find_packages


def readme():
    _ROOT = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(_ROOT, 'README.md')) as f:
        return f.read()


setup(name='aws-cicd',
      version='0.1.0',
      description="An API service for test CICD",
      author='takeshi.miao',
      author_email='takeshi.miao@gmail.com',
      url='https://github.com/takeshimiao/aws-cicd',
      packages=find_packages(exclude=("tests", "lambdas")),
      package_dir={'api': 'api'},
      package_data={'': ['conf/*']},
      long_description=readme(),
      install_requires=['bottle==0.12.13', 'boto3==1.4.4'],
      test_suite='tests',
      tests_require=['nose']
      )
