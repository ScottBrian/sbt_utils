#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 00:09:16 2020

@author: Scott Tuttle
"""

from setuptools import setup, find_packages

with open('README.rst', 'r') as readme:
    long_description = readme.read()


setup(
      name='sbt_utils',
      version='1.0.0',
      author='Scott Tuttle',
      author_email='sbtuttle@outlook.com',
      description='Print header/trailure utilities',
      long_description=long_description,
      long_description_content_type='text/x-rst',
      url='https://github.com/ScottBrian/sbt_utils.git',
      classifiers=[
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Licence :: OSI Approved :: MIT Licence',
          'Operating System :: POSIX :: Linux'
                  ],
      project_urls={
          'Source': 'https://github.com/ScottBrian/sbt_utils.git'},
      python_requires='>=3.6',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      install_requires=['wrapt'],
      package_data={"sbt_utils": ["__init__.pyi", "py.typed"]},
      zip_safe=False
     )
