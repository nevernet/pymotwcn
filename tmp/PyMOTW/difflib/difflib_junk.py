#!/usr/bin/env python
#
# Copyright 2007 Doug Hellmann.
#
#
#                         All Rights Reserved
#
# Permission to use, copy, modify, and distribute this software and
# its documentation for any purpose and without fee is hereby
# granted, provided that the above copyright notice appear in all
# copies and that both that copyright notice and this permission
# notice appear in supporting documentation, and that the name of Doug
# Hellmann not be used in advertising or publicity pertaining to
# distribution of the software without specific, written prior
# permission.
#
# DOUG HELLMANN DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
# INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN
# NO EVENT SHALL DOUG HELLMANN BE LIABLE FOR ANY SPECIAL, INDIRECT OR
# CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
# OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
# CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

"""Using the junk filter feature.

This example is taken from the source for difflib.py.

"""

__version__ = "$Id: difflib_junk.py 1882 2009-01-04 15:38:33Z dhellmann $"
#end_pymotw_header

from difflib import SequenceMatcher

A = " abcd"
B = "abcd abcd"

print 'A = "%s"' % A
print 'B = "%s"' % B

s = SequenceMatcher(None, A, B)
i, j, k = s.find_longest_match(0, 5, 0, 9)
print 'isjunk=None     :', (i, j, k), '"%s"' % A[i:i+k], '"%s"' % B[j:j+k]

s = SequenceMatcher(lambda x: x==" ", A, B)
i, j, k = s.find_longest_match(0, 5, 0, 9)
print 'isjunk=(x==" ") :', (i, j, k), '"%s"' % A[i:i+k], '"%s"' % B[j:j+k]

