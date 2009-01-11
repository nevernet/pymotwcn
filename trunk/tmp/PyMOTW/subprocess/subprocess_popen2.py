#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: subprocess_popen2.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import subprocess

print '\npopen2:'

proc = subprocess.Popen('cat -',
                        shell=True,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        )
stdout_value = proc.communicate('through stdin to stdout')[0]
print '\tpass through:', repr(stdout_value)
