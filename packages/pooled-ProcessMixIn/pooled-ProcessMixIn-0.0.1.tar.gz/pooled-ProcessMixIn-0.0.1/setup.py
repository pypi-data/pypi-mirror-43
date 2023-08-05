#! /usr/bin/python

# review classifiers http://pypi.python.org/pypi?%3Aaction=list_classifiers

import sys
import os

from setuptools import setup

import pooledProcessMixin

setup(name='pooled-ProcessMixIn',
      version='0.0.1',
      description='A Pool of processes and threads Mix-in for socketserver.',
      long_description=pooledProcessMixin.__doc__,
      author='Oleg Lupats',
      author_email='oleglupats@gmail.com',
      url='https://github.com/oleglpts/python-PooledProcessMixIn',
      packages=['pooledProcessMixin'],
      data_files=[('', ('README.md', 'TODO')), ('examples', ('examples/demo.py', 'examples/wsgi-demo.py'))],
      license='PSFL',
      platforms='any',
      classifiers=['License :: OSI Approved :: Python Software Foundation License',
                   'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
                   'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
                   'Topic :: Internet :: WWW/HTTP :: WSGI :: Server',
                   'Topic :: Software Development :: Libraries',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.5',
                   ],
      )
