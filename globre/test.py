# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# auth: metagriffin <mg.github@uberdev.org>
# date: 2013/09/22
# copy: (C) Copyright 2013-EOT metagriffin -- see LICENSE.txt
#------------------------------------------------------------------------------
# This software is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This software is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see http://www.gnu.org/licenses/.
#------------------------------------------------------------------------------

import unittest, re

import globre

#------------------------------------------------------------------------------
class TestGlobre(unittest.TestCase):

  if not hasattr(unittest.TestCase, 'assertIsNone'):
    def assertIsNone(self, *args, **kwargs):
      """Basic version of unittest.assertIsNotNone for Python 2.6 unittest."""
      return self.assertEqual(None, *args, **kwargs)

  if not hasattr(unittest.TestCase, 'assertIsNotNone'):
    def assertIsNotNone(self, *args, **kwargs):
      """Basic version of unittest.assertIsNotNone for Python 2.6 unittest."""
      return self.assertNotEqual(None, *args, **kwargs)


  #----------------------------------------------------------------------------
  def test_tokenizer(self):
    self.assertEqual(
      list(globre.Tokenizer('/foo/bar').tokens()),
      [('literal', '/foo/bar', 0, 8)])
    self.assertEqual(
      list(globre.Tokenizer('/foo\/bar').tokens()),
      [('literal', '/foo/bar', 0, 9)])
    self.assertEqual(
      list(globre.Tokenizer('/foo/*/bar').tokens()),
      [('literal', '/foo/', 0, 5),
       ('multiple', '*', 5, 6),
       ('literal', '/bar', 6, 10),
       ])
    self.assertEqual(
      list(globre.Tokenizer('/foo/**/bar/*.txt').tokens()),
      [('literal', '/foo/', 0, 5),
       ('any', '**', 5, 7),
       ('literal', '/bar/', 7, 12),
       ('multiple', '*', 12, 13),
       ('literal', '.txt', 13, 17),
       ])
    self.assertEqual(
      list(globre.Tokenizer('/foo/??.txt').tokens()),
      [('literal', '/foo/', 0, 5),
       ('single', '?', 5, 6),
       ('single', '?', 6, 7),
       ('literal', '.txt', 7, 11),
       ])
    self.assertEqual(
      list(globre.Tokenizer('/foo/??.txt').tokens()),
      [('literal', '/foo/', 0, 5),
       ('single', '?', 5, 6),
       ('single', '?', 6, 7),
       ('literal', '.txt', 7, 11),
       ])
    self.assertEqual(
      list(globre.Tokenizer(r'/foo/?\?.txt').tokens()),
      [('literal', '/foo/', 0, 5),
       ('single', '?', 5, 6),
       ('literal', '?.txt', 6, 12),
       ])
    self.assertEqual(
      list(globre.Tokenizer(r'/foo-[a-z0-9].txt').tokens()),
      [('literal', '/foo-', 0, 5),
       ('range', 'a-z0-9', 5, 13),
       ('literal', '.txt', 13, 17),
       ])
    self.assertEqual(
      list(globre.Tokenizer(r'/foo-{\\D{2,4\}}.txt').tokens()),
      [('literal', '/foo-', 0, 5),
       ('regex', r'\D{2,4}', 5, 16),
       ('literal', '.txt', 16, 20),
       ])

  #----------------------------------------------------------------------------
  def test_iswild(self):
    self.assertTrue(globre.iswild('/foo/bar/**.ini'))
    self.assertTrue(globre.iswild('/foo/bar-[0-9].ini'))
    self.assertFalse(globre.iswild('/foo/bar/conf.ini'))
    self.assertFalse(globre.iswild(r'\/foo\/bar\/conf.ini'))

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
    expr = globre.compile('/foo/bar/*.dir/**.ini', flags=0)
    self.assertEqual(expr.pattern, r'\/foo\/bar\/[^/]*?\.dir\/.*?\.ini')
    expr = globre.compile('/foo/bar-??-[a-z0-9].ini', flags=0)
    self.assertEqual(expr.pattern, r'\/foo\/bar\-[^/][^/]\-[a-z0-9]\.ini')

  #----------------------------------------------------------------------------
  def test_compile_exact(self):
    expr = globre.compile('/foo/bar/*.dir/**.ini', flags=globre.EXACT)
    self.assertEqual(expr.pattern, r'^\/foo\/bar\/[^/]*?\.dir\/.*?\.ini$')
    self.assertIsNotNone(expr.match('/foo/bar/a.dir/blue/conf.ini'))
    self.assertIsNotNone(expr.match('/foo/bar/a.dir/conf.ini'))
    self.assertIsNone(expr.match('/foo/bar/blue/a.dir/conf.ini'))
    self.assertIsNone(expr.match('/foo/bar/a.dir/conf.ini.x'))
    self.assertIsNone(expr.match('/x/foo/bar/a.dir/conf.ini'))

  #----------------------------------------------------------------------------
  def test_prefix(self):
    self.assertEqual(globre.compile('/foo/bar', split_prefix=True)[0], '/foo/bar')
    self.assertEqual(globre.compile('/foo/b**', split_prefix=True)[0], '/foo/b')
    self.assertEqual(globre.compile('??/foo/b**', split_prefix=True)[0], '')

  #----------------------------------------------------------------------------
  def test_complete(self):
    expr = globre.compile(r'/foo[0-9a-f]/*/bar\[??\]/{\\D{2,4\}}/**.txt')
    self.assertEqual(
      expr.pattern,
      r'\/foo[0-9a-f]\/[^/]*?\/bar\[[^/][^/]\]\/\D{2,4}\/.*?\.txt')
    self.assertIsNotNone(expr.match('/foo6/zog/bar[16]/abra/cadabra.txt'))

  #----------------------------------------------------------------------------
  def test_sep_compile(self):
    self.assertEqual(
      globre.compile('!foo!bar!*.dir!**.ini', sep='!').pattern,
      r'\!foo\!bar\![^\!]*?\.dir\!.*?\.ini')

  #----------------------------------------------------------------------------
  def test_sep_default(self):
    self.assertIsNotNone(globre.match('/foo/**.ini', '/foo/bar/conf.ini'))
    self.assertIsNone(globre.match('/foo/**.ini', '\\foo\\bar\\conf.ini'))
    self.assertIsNotNone(globre.match(':foo:**.ini', ':foo:bar:conf.ini'))
    self.assertIsNone(globre.match('/foo/*.ini', '/foo/bar/conf.ini'))
    self.assertIsNone(globre.match('/foo/*.ini', '\\foo\\bar\\conf.ini'))
    self.assertIsNotNone(globre.match(':foo:*.ini', ':foo:bar:conf.ini'))

  #----------------------------------------------------------------------------
  def test_sep_alternate(self):
    self.assertIsNotNone(globre.match('/foo/**.ini', '/foo/bar/conf.ini', sep='/'))
    self.assertIsNotNone(globre.match('\\\\foo\\\\**.ini', '\\foo\\bar\\conf.ini', sep='\\'))
    self.assertIsNotNone(globre.match(':foo:**.ini', ':foo:bar:conf.ini', sep=':'))
    self.assertIsNone(globre.match('/foo/*.ini', '/foo/bar/conf.ini', sep='/'))
    self.assertIsNone(globre.match('\\\\foo\\\\*.ini', '\\foo\\bar\\conf.ini', sep='\\'))
    self.assertIsNone(globre.match(':foo:*.ini', ':foo:bar:conf.ini', sep=':'))

  #----------------------------------------------------------------------------
  def test_sep_multi(self):
    self.assertIsNotNone(globre.match('/foo/**.ini', '/foo/bar/conf.ini', sep='/\\'))
    self.assertIsNotNone(globre.match('/foo/**.ini', '\\foo\\bar\\conf.ini', sep='/\\'))
    self.assertIsNotNone(globre.match('/foo/**.ini', '/foo\\bar/conf.ini', sep='/\\'))
    self.assertIsNotNone(globre.match('\\\\foo\\\\**.ini', '\\foo\\bar\\conf.ini', sep='/\\'))
    self.assertIsNotNone(globre.match('\\\\foo\\\\**.ini', '/foo/bar/conf.ini', sep='/\\'))
    self.assertIsNotNone(globre.match('\\\\foo/**.ini', '\\foo\\bar\\conf.ini', sep='/\\'))
    self.assertIsNotNone(globre.match('\\\\foo/**.ini', '/foo\\bar/conf.ini', sep='/\\'))
    self.assertIsNone(globre.match('/foo/*.ini', '/foo/bar/conf.ini', sep='/\\'))
    self.assertIsNone(globre.match('/foo/*.ini', '\\foo\\bar\\conf.ini', sep='/\\'))
    self.assertIsNone(globre.match('/foo/*.ini', '/foo\\bar/conf.ini', sep='/\\'))
    self.assertIsNone(globre.match('\\\\foo\\\\*.ini', '\\foo\\bar\\conf.ini', sep='/\\'))
    self.assertIsNone(globre.match('\\\\foo\\\\*.ini', '/foo/bar/conf.ini', sep='/\\'))
    self.assertIsNone(globre.match('\\\\foo/*.ini', '\\foo\\bar\\conf.ini', sep='/\\'))
    self.assertIsNone(globre.match('\\\\foo/*.ini', '/foo\\bar/conf.ini', sep='/\\'))


#------------------------------------------------------------------------------
# end of $Id$
# $ChangeLog$
#------------------------------------------------------------------------------
