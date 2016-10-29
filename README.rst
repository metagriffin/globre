==========================
Glob-Like Pattern Matching
==========================

Converts a glob-matching pattern to a regular expression, using Apache
Cocoon style rules (with some extensions).

TL;DR
=====

Install:

.. code:: bash

  $ pip install globre

Use:

.. code:: python

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
allows most characters to match themselves, with the following
sequences having special meanings:

=========  ====================================================================
Sequence   Meaning
=========  ====================================================================
``?``      Matches any single character except the slash
           ('/') character.
``*``      Matches zero or more characters *excluding* the slash
           ('/') character, e.g. ``/etc/*.conf`` which will *not*
           match "/etc/foo/bar.conf".
``**``     Matches zero or more characters *including* the slash
           ('/') character, e.g. ``/lib/**.so`` which *will*
           match "/lib/foo/bar.so".
``\``      Escape character used to precede any of the other special
           characters (in order to match them literally), e.g.
           ``foo\?`` will match "foo" followed by a literal question mark.
``[...]``  Matches any character in the specified regex-style character range,
           e.g. ``foo[0-9A-F].conf``.
``{...}``  Inlines a regex expression, e.g. ``foo-{\\D{2,4\}}.txt`` which
           will match "foo-bar.txt" but not "foo-012.txt".
=========  ====================================================================

The `globre` package exports the following functions:

* ``globre.match(pattern, string, sep=None, flags=0)``:

  Tests whether or not the glob `pattern` matches the `string`. If it
  does, a `re.MatchObject` is returned, otherwise ``None``. The `string`
  must be matched in its entirety. See `globre.compile` for details on
  the `sep` and `flags` parameters. Example:

  .. code:: python

    globre.match('/etc/**.conf', '/etc/rsyslog.conf')
    # => truthy

* ``globre.search(pattern, string, sep=None, flags=0)``:

  Similar to `globre.match`, but the pattern does not need to match
  the entire string. Example:

  .. code:: python

    globre.search('lib/**.so', '/var/lib/python/readline.so.6.2')
    # => truthy

* ``globre.compile(pattern, sep=None, flags=0, split_prefix=False)``:

  Compiles the specified `pattern` into a matching object that has the
  same API as the regular expression object returned by `re.compile`.

  The `sep` parameter specifies the hierarchical path component
  separator to use. By default, it uses the unix-style forward-slash
  separator (``"/"``), but can be overriden to be a sequence of
  alternative valid hierarchical path component separator characters.
  Note that although `sep` *could* be set to both forward- and back-
  slashes (i.e. ``"/\\"``) to, theoretically, support either unix- and
  windows-style path components, this has the significant flaw that
  then *both* characters can be used within the same path as
  separators.

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

  .. code:: python

    prefix, expr = globre.compile('/path/to**.ini', split_prefix=True)
    # prefix => '/path/to'

    names = [
      '/path/to/file.txt',
      '/path/to/config.ini',
      '/path/to/subdir/otherfile.txt',
      '/path/to/subdir/base.ini',
    ]

    for name in names:
      if not expr.match(name):
        # ignore the two ".txt" files
        continue
      # and do something with:
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

* The `glob` module does not provide an alternate hierarchy separator
  beyond ``/`` or ``\\``.
