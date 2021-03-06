========
urlparse
========
.. module:: urlparse
    :synopsis: Split URL into component pieces.

:Module: urlparse
:Purpose: Split URL into component pieces.
:Python Version: since 1.4
:Abstract:

    The urlparse module provides an interface for splitting up Uniform
    Resource Locator strings into their parts.

Description
===========

The urlparse module provides functions for breaking URLs down into their
component parts, as defined by the relevant RFCs.

Parsing
=======

The return value from the urlparse function is an object which acts like a
tuple with 6 elements.

::

    from urlparse import urlparse
    parsed = urlparse('http://netloc/path;parameters?query=argument#fragment')
    print parsed

The parts of the URL available through the tuple interface are the scheme,
network location, path, parameters, query, and fragment. In this example, I
use "http" for the scheme since "scheme" is not a valid scheme.

::

    $ python urlparse_urlparse.py 
    ('http', 'netloc', '/path', 'parameters', 'query=argument', 'fragment')


Although the return value acts like a tuple, it is really a subclass of tuple
which supports accessing the parts of the URL via named attributes instead of
indexes. That's especially useful if, like me, you can't remember the index
order. In addition to being easier to use for the programmer, the attribute
API also offers access to several values not available in the tuple API.

::

    from urlparse import urlparse
    parsed = urlparse('http://user:pass@NetLoc:80/path;parameters?query=argument#fragment')
    print 'scheme  :', parsed.scheme
    print 'netloc  :', parsed.netloc
    print 'path    :', parsed.path
    print 'params  :', parsed.params
    print 'query   :', parsed.query
    print 'fragment:', parsed.fragment
    print 'username:', parsed.username
    print 'password:', parsed.password
    print 'hostname:', parsed.hostname, '(netloc in lower case)'
    print 'port    :', parsed.port

The username and password are available when present and None when not. The
hostname is the same value as netloc, but all lower case letters are enforced.
And the port is converted to an integer when present and None when not.

::

    $ python urlparse_urlparseattrs.py 
    scheme  : http
    netloc  : user:pass@NetLoc:80
    path    : /path
    params  : parameters
    query   : query=argument
    fragment: fragment
    username: user
    password: pass
    hostname: netloc (netloc in lower case)
    port    : 80

The urlsplit function is an alternative to urlparse. It does not split the
parameters from the URL. This is useful for URLs following RFC 2396, which
supports parameters for each segment of the path. 

::

    from urlparse import urlsplit
    parsed = urlsplit('http://user:pass@NetLoc:80/path;parameters/path2;parameters2?query=argument#fragment')
    print parsed
    print 'scheme  :', parsed.scheme
    print 'netloc  :', parsed.netloc
    print 'path    :', parsed.path
    print 'query   :', parsed.query
    print 'fragment:', parsed.fragment
    print 'username:', parsed.username
    print 'password:', parsed.password
    print 'hostname:', parsed.hostname, '(netloc in lower case)'
    print 'port    :', parsed.port

Since the parameters are not split out, the tuple API will show 5 elements
instead of 6, and there is no params attribute.

::

    $ python urlparse_urlsplit.py 
    ('http', 'user:pass@NetLoc:80', '/path;parameters/path2;parameters2', 'query=argument', 'fragment')
    scheme  : http
    netloc  : user:pass@NetLoc:80
    path    : /path;parameters/path2;parameters2
    query   : query=argument
    fragment: fragment
    username: user
    password: pass
    hostname: netloc (netloc in lower case)
    port    : 80

To simply strip the fragment identifier from a URL, as you might need to do to
find a base page name from a URL, use urldefrag.

::

    from urlparse import urldefrag
    original = 'http://netloc/path;parameters?query=argument#fragment'
    print original
    url, fragment = urldefrag(original)
    print url
    print fragment

The return value is a tuple containing the base URL and the fragment.

::

    $ python urlparse_urldefrag.py
    http://netloc/path;parameters?query=argument#fragment
    http://netloc/path;parameters?query=argument
    fragment

Unparsing
=========

There are several ways to assemble a split URL back together into a single
string. The parsed URL object has a geturl() method.

::

    from urlparse import urlparse
    original = 'http://netloc/path;parameters?query=argument#fragment'
    print 'ORIG  :', original
    parsed = urlparse(original)
    print 'PARSED:', parsed.geturl()

Of course, it only works on the object returned by urlparse or urlsplit.

::

    $ python urlparse_geturl.py 
    ORIG  : http://netloc/path;parameters?query=argument#fragment
    PARSED: http://netloc/path;parameters?query=argument#fragment

If you have a tuple of values, you can use urlunparse() to assemble it into a
URL.

::

    from urlparse import urlparse, urlunparse
    original = 'http://netloc/path;parameters?query=argument#fragment'
    print 'ORIG  :', original
    parsed = urlparse(original)
    print 'PARSED:', type(parsed), parsed
    t = parsed[:]
    print 'TUPLE :', type(t), t
    print 'NEW   :', urlunparse(t)

While the ParseResult returned by urlparse can be used as a tuple, in this
example I explicitly create a new tuple to show that urlunparse works with
normal tuples, too.

::

    $ python urlparse_urlunparse.py 
    ORIG  : http://netloc/path;parameters?query=argument#fragment
    PARSED:  ('http', 'netloc', '/path', 'parameters', 'query=argument', 'fragment')
    TUPLE :  ('http', 'netloc', '/path', 'parameters', 'query=argument', 'fragment')
    NEW   : http://netloc/path;parameters?query=argument#fragment

If the input URL included superfluous parts, those may be dropped from the
unparsed version of the URL.

::

    from urlparse import urlparse, urlunparse
    original = 'http://netloc/path;?#'
    print 'ORIG  :', original
    parsed = urlparse(original)
    print 'PARSED:', type(parsed), parsed
    t = parsed[:]
    print 'TUPLE :', type(t), t
    print 'NEW   :', urlunparse(t)

In this case, the parameters, query, and fragment are all missing in the
original URL. The new URL does not look the same as the original, but is
equivalent according to the standard.

::

    $ python urlparse_urlunparseextra.py 
    ORIG  : http://netloc/path;?#
    PARSED:  ('http', 'netloc', '/path', '', '', '')
    TUPLE :  ('http', 'netloc', '/path', '', '', '')
    NEW   : http://netloc/path

Joining
=======

In addition to parsing URLs, the urlparse module includes the urljoin()
function for constructing absolute URLs from relative fragments.

::

    from urlparse import urljoin
    print urljoin('http://www.example.com/path/file.html', 'anotherfile.html')
    print urljoin('http://www.example.com/path/file.html', '../anotherfile.html')

Notice that the relative portion of the path ("../") is taken into account
when the second URL is computed.

::

    $ python urlparse_urljoin.py
    http://www.example.com/path/anotherfile.html
    http://www.example.com/anotherfile.html


