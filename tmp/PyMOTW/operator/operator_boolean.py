#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: operator_boolean.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

from operator import *

a = -1
b = 5

print 'a =', a
print 'b =', b

print 'not_(a):', not_(a)
print 'truth(a):', truth(a)
print 'is_(a, b):', is_(a,b)
print 'is_not(a, b):', is_not(a,b)