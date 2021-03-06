#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: SimpleXMLRPCServer_introspection.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

from SimpleXMLRPCServer import SimpleXMLRPCServer, list_public_methods
import os
import inspect

server = SimpleXMLRPCServer(('localhost', 9000), logRequests=True)
server.register_introspection_functions()

class DirectoryService:
    
    def _listMethods(self):
        return list_public_methods(self)

    def _methodHelp(self, method):
        f = getattr(self, method)
        return inspect.getdoc(f)
    
    def list(self, dir_name):
        """list(dir_name) => [<filenames>]
        
        Returns a list containing the contents of the named directory.
        """
        return os.listdir(dir_name)

server.register_instance(DirectoryService())

try:
    print 'Use Control-C to exit'
    server.serve_forever()
except KeyboardInterrupt:
    print 'Exiting'