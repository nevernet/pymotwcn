#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Test properties of a file.
"""

__version__ = "$Id: ospath_tests.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import os.path

for file in [ __file__, os.path.dirname(__file__), '/', './broken_link']:
    print 'File        :', file
    print 'Absolute    :', os.path.isabs(file)
    print 'Is File?    :', os.path.isfile(file)
    print 'Is Dir?     :', os.path.isdir(file)
    print 'Is Link?    :', os.path.islink(file)
    print 'Mountpoint? :', os.path.ismount(file)
    print 'Exists?     :', os.path.exists(file)
    print 'Link Exists?:', os.path.lexists(file)
    print
