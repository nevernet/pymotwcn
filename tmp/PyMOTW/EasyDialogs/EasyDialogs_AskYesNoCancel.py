#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2008 Doug Hellmann All rights reserved.
#
"""
"""

__version__ = "$Id: EasyDialogs_AskYesNoCancel.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

import EasyDialogs

valid_responses = { 1:'yes',
                    0:'no',
                    -1:'cancel',
                    }

response = EasyDialogs.AskYesNoCancel('Select an option')
print 'You selected:', valid_responses[response]
