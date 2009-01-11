#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: EasyDialogs_GetArgv.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import EasyDialogs

arguments = EasyDialogs.GetArgv([ 
        ('c=', 'program passed in as string (terminates option list)'),
        ('d', 'Debug'),
        ('E', 'Ignore environment variables'),
        ('i', 'Inspect interactively after running'),
        ('m=', 'run library module as a script (terminates option list)'),
        ('O', 'Optimize generated bytecode'),
        ('Q=', 'division options: -Qold (default), -Qwarn, -Qwarnall, -Qnew'),
        ('S', "don't imply 'import site' on initialization"),
        ('t', 'issue warnings about inconsistent tab usage'),
        ('tt', 'issue errors about inconsistent tab usage'),
        ('u', 'unbuffered binary stdout and stderr'),
        ('v', 'verbose (trace import statements)'),
        ('V', 'print the Python version number and exit'),
        ('W=', 'warning control  (arg is action:message:category:module:lineno)'),
        ('x', 'skip first line of source, allowing use of non-Unix forms of #!cmd'),
        ],
        commandlist=[('python', 'Default Interpreter'),
                     ('python2.5', 'Python 2.5'),
                     ('pyhton2.4', 'Python 2.4'),
                     ],
        addoldfile=True,
        addnewfile=False,
        addfolder=False,
        )
print arguments