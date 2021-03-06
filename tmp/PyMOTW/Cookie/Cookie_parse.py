#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: Cookie_parse.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import Cookie

HTTP_COOKIE = r'integer=5; string_with_quotes="He said, \"Hello, World!\""'

print 'From constructor:'
c = Cookie.SimpleCookie(HTTP_COOKIE)
print c

print
print 'From load():'
c = Cookie.SimpleCookie()
c.load(HTTP_COOKIE)
print c
