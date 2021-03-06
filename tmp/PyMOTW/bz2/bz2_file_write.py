#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: bz2_file_write.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import bz2
import os

output = bz2.BZ2File('example.txt.bz2', 'wb')
try:
    output.write('Contents of the example file go here.\n')
finally:
    output.close()

os.system('ls -l example.txt.bz2')
os.system('file example.txt.bz2')
