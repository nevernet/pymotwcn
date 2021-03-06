==============================================================
fnmatch -- Compare filenames against Unix-style glob patterns.
==============================================================

.. module:: fnmatch
    :synopsis: Compare filenames against Unix-style glob patterns.

:Purpose: Handle Unix-style filename comparison with the fnmatch module.
:Python Version: 1.4 and later.

The fnmatch module is used to compare filenames against glob-style patterns
such as used by Unix shells.

Simple Matching
===============

fnmatch() compares a single filename against a pattern and returns a boolean
indicating whether or not they match. If the operating system uses a
case-insensitive filesystem, the comparison is not case sensitive. Otherwise
it is.

::

    import fnmatch
    import os

    pattern = 'fnmatch_*.py'
    print 'Pattern :', pattern
    print

    files = os.listdir('.')
    for name in files:
        print 'Filename: %-25s %s' % (name, fnmatch.fnmatch(name, pattern))


In this example, the pattern matches all files starting with 'fnmatch_' and
ending in '.py'.

::

    $ python fnmatch_fnmatch.py
    Pattern : fnmatch_*.py

    Filename: .svn                      False
    Filename: __init__.py               False
    Filename: fnmatch_filter.py         True
    Filename: fnmatch_fnmatch.py        True
    Filename: fnmatch_fnmatchcase.py    True
    Filename: fnmatch_translate.py      True

To force a case-sensitive comparison, regardless of the filesystem and
operating system settings, use fnmatchcase().

::

    import fnmatch
    import os

    pattern = 'FNMATCH_*.PY'
    print 'Pattern :', pattern
    print

    files = os.listdir('.')

    for name in files:
        print 'Filename: %-25s %s' % (name, fnmatch.fnmatchcase(name, pattern))

Since my laptop uses a case-sensitive filesystem, no files match the modified
pattern.

::

    $ python fnmatch_fnmatchcase.py
    Pattern : FNMATCH_*.PY

    Filename: .svn                      False
    Filename: __init__.py               False
    Filename: fnmatch_filter.py         False
    Filename: fnmatch_fnmatch.py        False
    Filename: fnmatch_fnmatchcase.py    False
    Filename: fnmatch_translate.py      False

Filtering
=========

To test a sequence of filenames, you can use filter(). It returns a list of
the names that match the pattern argument.

::

    import fnmatch
    import os

    pattern = 'fnmatch_*.py'
    print 'Pattern :', pattern

    files = os.listdir('.')
    print 'Files   :', files

    print 'Matches :', fnmatch.filter(files, pattern)

In this example, filter() returns the list of names of the example source
files associated with this post.

::

    $ python fnmatch_filter.py
    Pattern : fnmatch_*.py
    Files   : ['.svn', '__init__.py', 'fnmatch_filter.py', 'fnmatch_fnmatch.py', 'fnmatch_fnmatchcase.py', 'fnmatch_translate.py']
    Matches : ['fnmatch_filter.py', 'fnmatch_fnmatch.py', 'fnmatch_fnmatchcase.py', 'fnmatch_translate.py']

Translating Patterns
====================

Internally, fnmatch converts the glob pattern to a regular expression and uses
the re module to compare the name and pattern. The translate() function is the
public API for converting glob patterns to regular expressions.

::

    import fnmatch

    pattern = 'fnmatch_*.py'
    print 'Pattern :', pattern
    print 'Regex   :', fnmatch.translate(pattern)

Notice that some of the characters are escaped to make a valid expression.

::

    $ python fnmatch_translate.py
    Pattern : fnmatch_*.py
    Regex   : fnmatch\_.*\.py$

.. seealso::

    `fnmatch <http://docs.python.org/library/fnmatch.html>`_
        The standard library documentation for this module.
