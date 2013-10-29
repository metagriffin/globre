# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# auth: metagriffin <metagriffin@uberdev.org>
# date: 2013/09/22
# copy: (C) CopyLoose 2013 UberDev <hardcore@uberdev.org>, No Rights Reserved.
#------------------------------------------------------------------------------

import re

# new flags that apply to globs only...
EXACT = 1 << 10
E     = EXACT

WILDCHARS = '?*[{\\'

#------------------------------------------------------------------------------
def iswild(pattern):
  for wild in WILDCHARS:
    if wild in pattern:
      return True
  return False

#------------------------------------------------------------------------------
def compile(pattern, flags=0):
  '''
  Converts a glob-matching pattern (using Apache Cocoon style rules)
  to a regular expression, which basically means that the following
  characters have special meanings:

  * ``?``:   matches any single character excluding the slash ('/') character
  * ``*``:   matches zero or more characters excluding the slash ('/') character
  * ``**``:  matches zero or more characters including the slash ('/') character
  * ``\``:   escape character used to precede any of the others for a literal

  TODO: the backslash-escaping is not implemented.

  TODO: add support for [...] character ranges.

  TODO: add support fo {...} explicit regex.

  TODO: implement `flags`.

  The `flags` bit mask can contain all the standard `re` flags, in
  addition to the ``globre.EXACT`` flag. If EXACT is set, then the
  returned regex will include a leading '^' and trailing '$', meaning
  that the regex must match the entire string, from beginning to end.
  '''
  # todo: this is a poor-man's implementation... this could be
  #         a) more efficient
  #         b) implement escaping
  #         c) be more LR-parsing rigorous...

  # todo: all of that could be implemented using python's `shlex`...

  # 'encode' the special characters into non-regex-special characters
  pattern = pattern \
    .replace('Z', 'ZI') \
    .replace('?', 'ZQ') \
    .replace('**', 'ZA') \
    .replace('*', 'ZD')

  # escape all regex-sensitive characters
  pattern = re.escape(pattern)

  # and undo the 'encoding'
  pattern = pattern \
    .replace('ZD', '[^/]*?') \
    .replace('ZA', '.*?') \
    .replace('ZQ', '.') \
    .replace('ZI', 'Z')

  exact = flags & EXACT
  flags = flags & ~ EXACT

  return re.compile(( '^' + pattern + '$' ) if exact else pattern, flags=flags)

#------------------------------------------------------------------------------
def match(pattern, string, flags=0):
  flags |= EXACT
  return compile(pattern, flags=flags).match(string)

#------------------------------------------------------------------------------
def search(pattern, string, flags=0):
  flags &= ~ EXACT
  return compile(pattern, flags=flags).search(string)

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
