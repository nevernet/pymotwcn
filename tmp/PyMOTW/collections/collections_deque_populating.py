#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Adding items to a deque.
"""

__version__ = "$Id: collections_deque_populating.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import collections

# Add to the right
d = collections.deque()
d.extend('abcdefg')
print 'extend    :', d
d.append('h')
print 'append    :', d

# Add to the left
d = collections.deque()
d.extendleft('abcdefg')
print 'extendleft:', d
d.appendleft('h')
print 'appendleft:', d
