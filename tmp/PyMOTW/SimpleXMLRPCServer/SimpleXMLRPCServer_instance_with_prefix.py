#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: SimpleXMLRPCServer_instance_with_prefix.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

from SimpleXMLRPCServer import SimpleXMLRPCServer
import os
import inspect

server = SimpleXMLRPCServer(('localhost', 9000), logRequests=True)

def expose(f):
    "Decorator to set exposed flag on a function."
    f.exposed = True
    return f

def is_exposed(f):
    "Test whether another function should be publicly exposed."
    return getattr(f, 'exposed', False)

class MyService:
    PREFIX = 'prefix'

    def _dispatch(self, method, params):
        # Remove our prefix from the method name
        if not method.startswith(self.PREFIX + '.'):
            raise Exception('method "%s" is not supported' % method)
        
        method_name = method.partition('.')[2]
        func = getattr(self, method_name)            
        if not is_exposed(func):
            raise Exception('method "%s" is not supported' % method)
        
        return func(*params)

    @expose
    def public(self):
        return 'This is public'
        
    def private(self):
        return 'This is private'

server.register_instance(MyService())

try:
    print 'Use Control-C to exit'
    server.serve_forever()
except KeyboardInterrupt:
    print 'Exiting'