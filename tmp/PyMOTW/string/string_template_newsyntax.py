#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: string_template_newsyntax.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import re
import string

class MyTemplate(string.Template):
    delimiter = '{{'
    pattern = re.compile(r'''
    \{\{(?:
    (?P<escaped>\{\{)|
    (?P<named>[_a-z][_a-z0-9]*)\}\}|
    (?P<braced>[_a-z][_a-z0-9]*)\}\}|
    (?P<invalid>)
    )
    ''', re.VERBOSE | re.DOTALL)
    
t = MyTemplate('''
{{{{
{{var}}
''')

print 'MATCHES:', t.pattern.findall(t.template)
print 'SUBSTITUTED:', t.safe_substitute(var='replacement')