#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: uuid_uuid4.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import uuid

for i in xrange(3):
    print uuid.uuid4()
