#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: platform_architecture.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import platform

print 'interpreter:', platform.architecture()
print '/bin/ls    :', platform.architecture('/bin/ls')