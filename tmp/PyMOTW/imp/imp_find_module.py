#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: imp_find_module.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import imp
from imp_get_suffixes import module_types

print 'Package:'
f, filename, description = imp.find_module('example')
print module_types[description[2]], filename
print

print 'Sub-module:'
f, filename, description = imp.find_module('submodule', ['./example'])
print module_types[description[2]], filename
if f: f.close()
