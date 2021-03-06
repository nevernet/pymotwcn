#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Example using weakref.ref to manage a reference to an object
with a callback.
"""

__version__ = "$Id: weakref_ref_callback.py 1882 2009-01-04 15:38:33Z dhellmann $"

import weakref

class ExpensiveObject(object):
    def __del__(self):
        print '(Deleting %s)' % self
        
def callback(reference):
    """Invoked when referenced object is deleted"""
    print 'callback(', reference, ')'

obj = ExpensiveObject()
r = weakref.ref(obj, callback)

print 'obj:', obj
print 'ref:', r
print 'r():', r()

print 'deleting obj'
del obj
print 'r():', r()
