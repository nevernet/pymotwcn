=========
zipimport
=========
.. module:: zipimport
    :synopsis: Load Python code from inside ZIP archives.

:Module: zipimport
:Purpose: Load Python code from inside ZIP archives.
:Python Version: 2.3 and later
:Abstract:

    The zipimport module can be used to import and run Python code found
    inside ZIP archives.

Description
===========

The zipimport module implements the zipimporter class, which can be used to
find and load Python modules inside ZIP archives. The zipimporter supports the
"import hooks" API specified in `PEP 302`_; this is how Python Eggs work.

You probably won't need to use the zipimport module directly, since it is
possible to import directly from a ZIP archive as long as that archive appears
in your sys.path. However, it is interesting to see the features available.

Example
=======

For the examples this week, I'll reuse some of the code from last week's
discussion of zipfile to create an example ZIP archive containing some Python
modules. If you are experimenting with the sample code on your system, run
zipimport_make_example.zip before any of the rest of the examples. It will
create a ZIP archive containing all of the modules in the zipimport example
directory, along with some test data needed for the code below.

Finding a Module
================

Given the full name of a module, find_module() will try to locate that module
inside the ZIP archive.

::

    import zipimport

    importer = zipimport.zipimporter('zipimport_example.zip')

    for module_name in [ 'zipimport_find_module', 'not_there' ]:
        print module_name, ':', importer.find_module(module_name)

If the module is found, the zipimporter instance is returned. Otherwise, None
is returned.

::

    $ python zipimport_find_module.py
    zipimport_find_module : <zipimporter object "zipimport_example.zip">
    not_there : None

Accessing Code
==============

The get_code() method loads the code object for a module from the archive.

::

    importer = zipimport.zipimporter('zipimport_example.zip')
    code = importer.get_code('zipimport_get_code')
    print code

The code object is not the same as a module object.

::

    $ python zipimport_get_code.py
    <code object <module> at 0x57530, file "./zipimport_get_code.py", line 28>

To load the code as a usable module, use load_module() instead.

::

    importer = zipimport.zipimporter('zipimport_example.zip')
    module = importer.load_module('zipimport_get_code')
    print 'Name   :', module.__name__
    print 'Loader :', module.__loader__
    print 'Code   :', module.code

The result is a module object as though the code had been loaded from a
regular import:

::

    $ python zipimport_load_module.py
    <code object <module> at 0x57968, file "./zipimport_get_code.py", line 28>
    Name   : zipimport_get_code
    Loader : <zipimporter object "zipimport_example.zip">
    Code   : <code object <module> at 0x57968, file "./zipimport_get_code.py", line 28>

Source
======

As with the inspect module, it is possible to retrieve the source code for a
module from the ZIP archive, if the archive includes the source. In the case
of the example, only zipimport_get_source.py is added to zipimport_example.zip
(the rest of the modules are just the .pyc files).

::

    importer = zipimport.zipimporter('zipimport_example.zip')
    for module_name in ['zipimport_get_code', 'zipimport_get_source']:
        source = importer.get_source(module_name)
        print '=' * 80
        print module_name
        print '=' * 80
        print source
        print

If the source for a module is not available, get_source() returns None.

::

    $ python zipimport_get_source.py
    ================================================================================
    zipimport_get_code
    ================================================================================
    None

    ================================================================================
    zipimport_get_source
    ================================================================================
    #!/usr/bin/env python
    #
    # ... some lines omitted for brevity ...
    #
    import zipimport

    importer = zipimport.zipimporter('zipimport_example.zip')
    source = importer.get_source('zipimport_get_code')
    print source

Packages
========

To determine if a name refers to a package instead of a regular module, use
is_package().

::

    importer = zipimport.zipimporter('zipimport_example.zip')
    for name in ['zipimport_is_package', 'example_package']:
        print name, importer.is_package(name)

In this case, zipimport_is_package came from a module and the example_package
is, well, a package.

::

    $ python zipimport_is_package.py
    zipimport_is_package False
    example_package True

Data
====

There are times when source modules or packages need to be distributed with
non-code data. Images, configuration files, default data, and test fixtures
are just a few examples of this. Frequently, the module __path__ is used to
find these data files relative to where the code is installed.

For example, with a normal module you might do something like:

::

    import os
    import example_package
    data_filename = os.path.join(os.path.dirname(example_package.__file__), 
                                 'README.txt')
    print data_filename, ':'
    print open(data_filename, 'rt').read()

The output will look something like this, with the path changed based on where
the PyMOTW sample code is on your filesystem.

::

    $ python zipimport_get_data_nozip.py /Users/dhellmann/Documents/PyMOTW/in_progress/zipimport/example_package/README.txt :
    This file represents sample data which could be embedded in the ZIP
    archive.  You could include a configuration file, images, or any other
    sort of non-code data.

If the example_package is imported from the ZIP archive instead of the
filesystem, that method does not work:

::

    import sys
    sys.path.insert(0, 'zipimport_example.zip')

    import os
    import example_package
    print example_package.__file__
    data_filename = os.path.join(os.path.dirname(example_package.__file__), 
                                 'README.txt')
    print data_filename, ':'
    print open(data_filename, 'rt').read()

The __file__ of the package refers to the ZIP archive, and not a directory. So
we cannot just build up the path to the README.txt file.

::

    $ python zipimport_get_data_zip.pyzipimport_example.zip/example_package/__init__.pyc
    zipimport_example.zip/example_package/README.txt :
    Traceback (most recent call last):
      File "zipimport_get_data_zip.py", line 41, in 
        print open(data_filename, 'rt').read()
    IOError: [Errno 20] Not a directory: 'zipimport_example.zip/example_package/README.txt'

Instead, we need to use the get_data() method. We can access zipimporter
instance which loaded the module through the __loader__ attribute of the
imported module: 

::

    import sys
    sys.path.insert(0, 'zipimport_example.zip')

    import os
    import example_package
    print example_package.__file__
    print example_package.__loader__.get_data('example_package/README.txt')

::

    $ python zipimport_get_data.py
    zipimport_example.zip/example_package/__init__.pyc
    This file represents sample data which could be embedded in the ZIP
    archive.  You could include a configuration file, images, or any other
    sort of non-code data.

Although __loader__ is not set for modules not imported via zipimport.


References
==========

`PEP 302 <http://www.python.org/peps/pep-0302.html>`_ -- New Import Hooks

