#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Passing arguments to threads when they are created
"""

__version__ = "$Id: threading_simpleargs.py 1882 2009-01-04 15:38:33Z dhellmann $"

import threading

def worker(num):
    """thread worker function"""
    print 'Worker:', num
    return

threads = []
for i in range(5):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()
