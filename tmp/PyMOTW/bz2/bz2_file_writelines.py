#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: bz2_file_writelines.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import bz2
import itertools
import os

output = bz2.BZ2File('example_lines.txt.bz2', 'wb')
try:
    output.writelines(itertools.repeat('The same line, over and over.\n', 10))
finally:
    output.close()

os.system('bzcat example_lines.txt.bz2')
