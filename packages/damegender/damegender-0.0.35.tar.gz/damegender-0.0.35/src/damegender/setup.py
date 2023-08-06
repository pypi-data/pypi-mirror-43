#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2019  David Arroyo Menéndez

# Author: David Arroyo Menéndez <davidam@gnu.org>
# Maintainer: David Arroyo Menéndez <davidam@gnu.org>

# This file is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.

# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with GNU Emacs; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301 USA,

from setuptools import setup

def readme():
    with open('README.org') as f:
        return f.read()

setup(name='damegender',
      version='0.2',
      description='Gender Detection Tool by David Arroyo MEnéndez',
      long_description=readme(),
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: GPLv3 License",
          "Operating System :: OS Independent",
      ],
      keywords='gender repositories',
      url='http://github.com/davidam/damegender',
      author='David Arroyo Menéndez',
      author_email='davidam@gnu.org',
      license='GPLv3',
      packages=['damegender'],
      install_requires=[
          'markdown',
          'nltk',
          'perceval',
          'requests',
          'gender_guesser',
          'genderize',
          'numpy',
          'scikit-learn',
          'pyhyphen',
          'unidecode',
          'pandas',
          'matplotlib',
      ],
      test_suite='nose.collector',
      tests_require=['nose', 'nose-cover3'],
      entry_points={
          'console_scripts': ['funniest-joke=funniest.command_line:main'],
      },
      include_package_data=True,
      zip_safe=False)
