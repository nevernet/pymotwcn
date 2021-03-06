#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""Creating dates from existing objects.
"""

__version__ = "$Id: datetime_date_replace.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import datetime

d1 = datetime.date(2008, 3, 12)
print 'd1:', d1

d2 = d1.replace(year=2009)
print 'd2:', d2