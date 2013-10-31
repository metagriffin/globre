==========================
Glob-Like Pattern Matching
==========================

Converts a glob-matching pattern to a regular expression, using Apache
Cocoon style rules (with some extensions).

TL;DR
=====

Install:

.. code-block:: bash

  $ pip install globre

Use:

.. code-block:: python

  import globre

  names = [
    '/path/to/file.txt',
    '/path/to/config.ini',
    '/path/to/subdir/base.ini',
    ]

  txt_names = [name for name in names if globre.match('/path/to/*.txt', name)]
  assert txt_names == ['/path/to/file.txt']

  ini_names = [name for name in names if globre.match('/path/to/*.ini', name)]
  assert ini_names == ['/path/to/config.ini']

  all_ini_names = [name for name in names if globre.match('/path/to/**.ini', name)]
  assert all_ini_names == ['/path/to/config.ini', '/path/to/subdir/base.ini']


Details
=======

This package basically allows using unix shell-like filename globbing
to be used to match a string in a Python program. The glob matching
allows must characters to match themselves, with the following
sequences having special meanings:

=========  ====================================================================
Sequence   Meaning
=========  ====================================================================
``?``      Matches any single character except the slash
           ('/') character.
``*``      Matches zero or more characters *excluding* the slash
           ('/') character.
``**``     Matches zero or more characters *including* the slash
           ('/') character.
``\``      Escape character used to precede any of the other special
           characters (in order to insert it literally).
``[...]``  Matches any character in the specified regex-style range.
``{...}``  Inlines a regex expression.
=========  ====================================================================

The `globre` package exports the following functions:

* ``globre.match(pattern, string, flags=0)``:

  Tests whether or not the glob `pattern` matches the `string`. If it
  does, a `re.MatchObject` is returned, otherwise ``None``. The `string`
  must be matched in its entirety. See `globre.compile` for details on
  the `flags` parameter. Example:

  .. code-block:: python

    globre.match('/etc/**.conf', '/etc/rsyslog.conf')
    # => truthy

* ``globre.search(pattern, string, flags=0)``:

  Similar to `globre.match`, but the pattern does not need to match
  the entire string. Example:

  .. code-block:: python

    globre.search('lib/**.so', '/var/lib/python/readline.so.6.2')
    # => truthy

* ``globre.compile(pattern, flags=0, split_prefix=False)``:

  Compiles the specified `pattern` into a matching object that has the
  same API as the regular expression object returned by `re.compile`.

  The `flags` bit mask can contain all the standard `re` flags, in
  addition to the ``globre.EXACT`` flag. If EXACT is set, then the
  returned regex will include the equivalent of a leading '^' and
  trailing '$', meaning that the regex must match the entire string,
  from beginning to end.

  If `split_prefix` is truthy, the return value becomes a tuple with
  the first element set to any initial non-wildcarded string found in
  the pattern. The second element remains the regex object as before.
  For example, the pattern ``foo/**.ini`` would result in a tuple
  equivalent to ``('foo/', re.compile('foo/.*\\.ini'))``.

  Example:

  .. code-block:: python

    prefix, expr = globre.compile('/path/to**.ini', split_prefix=True)
    # prefix => '/path/to'

    names = [
      '/path/to/file.txt',
      '/path/to/config.ini',
      '/path/to/subdir/base.ini',
      ]

    for name in names:
      if not expr.match(name):
        continue
      # ... do something with:
      #   - /path/to/config.ini
      #   - /path/to/subdir/base.ini


What About the ``glob`` Module
==============================

This package is different from the standard Python `glob` module in
the following critical ways:

* The `glob` module operates on the actual filesystem; `globre` can be
  used to match both files on the filesystem as well as any other
  sources of strings to match.

* The `glob` module does not provide the ``**`` "descending" matcher.

* The `glob` module does not provide the ``{...}`` regular expression
  inlining feature.
