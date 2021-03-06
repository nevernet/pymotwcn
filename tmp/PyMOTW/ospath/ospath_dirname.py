#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Find the directory portion of a filename.
"""

__version__ = "$Id: ospath_dirname.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import os.path

for path in [ '/one/two/three', 
              '/one/two/three/',
              '/',
              '.',
              '']:
    print '"%s" : "%s"' % (path, os.path.dirname(path))