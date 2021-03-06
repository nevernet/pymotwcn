#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: subprocess_popen4.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import subprocess

print '\npopen4:'
proc = subprocess.Popen('cat -; echo ";to stderr" 1>&2',
                        shell=True,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        )
stdout_value, stderr_value = proc.communicate('through stdin to stdout\n')
print '\tcombined output:', repr(stdout_value)
