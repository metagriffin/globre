#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# auth: metagriffin <metagriffin@uberdev.org>
# date: 2013/10/28
# copy: (C) CopyLoose 2013 UberDev <hardcore@uberdev.org>, No Rights Reserved.
#------------------------------------------------------------------------------

import os, sys, setuptools
from setuptools import setup, find_packages

# require python 2.7+
if sys.hexversion < 0x02070000:
  raise RuntimeError('This package requires python 2.7 or better')

heredir = os.path.abspath(os.path.dirname(__file__))
def read(*parts, **kw):
  try:    return open(os.path.join(heredir, *parts)).read()
  except: return kw.get('default', '')

test_dependencies = [
  'nose                 >= 1.3.0',
  'coverage             >= 3.6',
  ]

dependencies = [
  'distribute           >= 0.6.24',
  ]

entrypoints = {
  # 'console_scripts': [
  #   'TODO:PROJNAME      = TODO:PROJNAME.cli:main',
  #   ],
  }

classifiers = [
  'Development Status :: 4 - Beta',
  # 'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'Programming Language :: Python',
  'Operating System :: OS Independent',
  'Natural Language :: English',
  'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
  ]

setup(
  name                  = 'globlib',
  version               = read('VERSION.txt', default='0.0.1').strip(),
  description           = 'A glob-like regular expression generation library.',
  long_description      = read('README.rst'),
  classifiers           = classifiers,
  author                = 'metagriffin',
  author_email          = 'mg.pypi@uberdev.org',
  url                   = 'http://github.com/metagriffin/globlib',
  keywords              = 'python glob pattern matching regular expression',
  packages              = find_packages(),
  platforms             = ['any'],
  include_package_data  = True,
  zip_safe              = True,
  install_requires      = dependencies,
  tests_require         = test_dependencies,
  test_suite            = 'globlib',
  entry_points          = entrypoints,
  license               = 'GPLv3+',
  )

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
