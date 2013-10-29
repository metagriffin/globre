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
def compile(pattern, split_prefix=False, flags=0):
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

  If `split_prefix` is truthy, the return value becomes a tuple with
  the first element set to any initial non-wildcarded string found in
  the pattern. The second element remains the regex object as before.
  For example, the pattern ``foo/**.ini`` would result in a tuple
  equivalent to ``('foo/', re.compile('foo/.*\\.ini'))``.

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

  # todo: this prefix extraction is ugly... improve
  prefix = None
  if split_prefix:
    idx = None
    for wild in WILDCHARS:
      if wild in pattern:
        if idx is None:
          idx = pattern.find(wild)
        else:
          idx = min(idx, pattern.find(wild))
    if idx is not None:
      prefix = pattern[:idx]
    else:
      prefix = pattern

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
  expr  = re.compile(( '^' + pattern + '$' ) if exact else pattern, flags=flags)

  if prefix is not None:
    return (prefix, expr)
  return expr

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
