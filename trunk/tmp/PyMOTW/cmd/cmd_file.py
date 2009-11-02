#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: cmd_file.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import cmd

class HelloWorld(cmd.Cmd):
    """Simple command processor example."""
    
    # Disable rawinput module use
    use_rawinput = False
    
    # Do not show a prompt after each command read
    prompt = ''
    
    def do_greet(self, line):
        print "hello,", line
    
    def do_EOF(self, line):
        return True

if __name__ == '__main__':
    import sys
    input = open(sys.argv[1], 'rt')
    try:
        HelloWorld(stdin=input).cmdloop()
    finally:
        input.close()