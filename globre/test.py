# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# auth: metagriffin <metagriffin@uberdev.org>
# date: 2013/09/22
# copy: (C) CopyLoose 2013 UberDev <hardcore@uberdev.org>, No Rights Reserved.
#------------------------------------------------------------------------------

import unittest, re

import globre

#------------------------------------------------------------------------------
class TestGlobre(unittest.TestCase):

  #----------------------------------------------------------------------------
  def test_iswild(self):
    self.assertTrue(globre.iswild('/foo/bar/**.ini'))
    self.assertTrue(globre.iswild('/foo/bar-[0-9].ini'))
    self.assertFalse(globre.iswild('/foo/bar/conf.ini'))

  #----------------------------------------------------------------------------
  def test_match(self):
    self.assertIsNotNone(globre.match('/foo/bar/**.ini', '/foo/bar/conf.ini'))
    self.assertIsNotNone(globre.match('/foo/bar/**.ini', '/foo/bar/a/b/c/conf.ini'))
    self.assertIsNone(globre.match('/foo/bar/**.ini', '/a/foo/bar/conf.ini'))
    self.assertIsNone(globre.match('/foo/bar/**.ini', '/foo/bar/conf.ini.txt'))
    self.assertIsNone(globre.match('/foo/bar/**.ini', '/foo/bar/conf.ini/zig.txt'))
    self.assertIsNone(globre.match('/foo/bar/**.ini', '/FOO/BAR/ZIP/CONF.INI'))
    self.assertIsNotNone(globre.match('/foo/bar/**.ini', '/FOO/BAR/ZIP/CONF.INI', flags=re.IGNORECASE))

  #----------------------------------------------------------------------------
  def test_search(self):
    self.assertIsNotNone(globre.search('/foo/bar/**.ini', '/foo/bar/conf.ini'))
    self.assertIsNotNone(globre.search('/foo/bar/**.ini', '/foo/bar/a/b/c/conf.ini'))
    self.assertIsNotNone(globre.search('/foo/bar/**.ini', '/a/foo/bar/conf.ini'))
    self.assertIsNotNone(globre.search('/foo/bar/**.ini', '/foo/bar/conf.ini.txt'))
    self.assertIsNotNone(globre.search('/foo/bar/**.ini', '/foo/bar/conf.ini/zig.txt'))
    self.assertIsNone(globre.search('/foo/bar/**.ini', '/foo/bar/conf.txt'))
    self.assertIsNone(globre.search('/foo/bar/**.ini', '/X/FOO/BAR/ZIP/CONF.INI'))
    self.assertIsNotNone(globre.search('/foo/bar/**.ini', '/X/FOO/BAR/ZIP/CONF.INI', flags=re.IGNORECASE))

  #----------------------------------------------------------------------------
  def test_compile(self):
    expr = globre.compile('/foo/bar/*.dir/**.ini', flags=globre.EXACT)
    self.assertIsNotNone(expr.match('/foo/bar/a.dir/blue/conf.ini'))
    self.assertIsNotNone(expr.match('/foo/bar/a.dir/conf.ini'))
    self.assertIsNone(expr.match('/foo/bar/blue/a.dir/conf.ini'))
    self.assertIsNone(expr.match('/foo/bar/a.dir/conf.ini.x'))
    self.assertIsNone(expr.match('/x/foo/bar/a.dir/conf.ini'))

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
