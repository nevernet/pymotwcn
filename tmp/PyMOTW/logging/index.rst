============================================================
logging -- Report status, error, and informational messages.
============================================================

.. module:: logging
    :synopsis: Report status, error, and informational messages.

:Purpose: Report status, error, and informational messages.
:Python Version: 2.3

The logging module defines a standard API for reporting errors and status
information from all of your modules. The key benefit of having the logging
API provided by a standard library module is that all python modules can
participate in logging, so your application log can include messages from
third-party modules.

It is, of course, possible to log messages with different verbosity levels or
to different destinations. Support for writing log messages to files, HTTP
GET/POST locations, email via SMTP, generic sockets, or OS-specific logging
mechanisms are all supported by the standard module. You can also create your
own log destination class if you have special requirements not met by any of
the built-in classes.

Logging to a File
=================

Most applications are probably going to want to log to a file, so let's start
with that case. Using the basicConfig() function, we can set up the default
handler so that debug messages are written to a file.

.. include:: logging_file_example.py
    :literal:
    :start-after: #end_pymotw_header

And now if we run the script and look at what we have, we should find the log
message:

::

    $ python logging_file_example.py
    FILE:
    DEBUG:root:This message should go to the log file


Rotating Log Files
==================

If you run the script repeatedly, the additional log messages are appended to
the file. To create a new file each time, you can pass a ``filemode`` argument to
``basicConfig()`` with a value of ``'w'``. Rather than managing the file size
yourself, though, it is simpler to use a RotatingFileHandler:

.. include:: logging_rotatingfile_example.py
    :literal:
    :start-after: #end_pymotw_header

The result should be 6 separate files, each with part of the log history for
the application:

::

    $ python logging_rotatingfile_example.py
    /tmp/logging_rotatingfile_example.out
    /tmp/logging_rotatingfile_example.out.1
    /tmp/logging_rotatingfile_example.out.2
    /tmp/logging_rotatingfile_example.out.3
    /tmp/logging_rotatingfile_example.out.4
    /tmp/logging_rotatingfile_example.out.5

The most current file is always ``/tmp/logging_rotatingfile_example.out``, and
each time it reaches the size limit it is renamed with the suffix ``.1``. Each of
the existing backup files is renamed to increment the suffix (``.1`` becomes ``.2``,
etc.) and the ``.5`` file is erased.

Obviously this example sets the log length much much too small as an extreme
example. You would want to set maxBytes to an appropriate value.

Verbosity Levels
================

Another useful feature of the logging API is the ability to produce different
messages at different log levels. This allows you to instrument your code with
debug messages, for example, but turning the log level down so that those
debug messages are not written for your production system.

========  =====
Level     Value
========  =====
CRITICAL  50
ERROR     40
WARNING   30
INFO      20
DEBUG     10
UNSET      0
========  =====

The logger, handler, and log message call each specify a level. The log
message is only emitted if the handler and logger are configured to emit
messages of that level or lower. For example, if a message is CRITICAL, and
the logger is set to ERROR, the message is emitted. If a message is a WARNING,
and the logger is set to produce only ERRORs, the message is not emitted.

.. include:: logging_level_example.py
    :literal:
    :start-after: #end_pymotw_header

Run the script with an argument like 'debug' or 'warning' to see which
messages show up at different levels:

::

    $ python logging_level_example.py debug
    DEBUG:root:This is a debug message
    INFO:root:This is an info message
    WARNING:root:This is a warning message
    ERROR:root:This is an error message
    CRITICAL:root:This is a critical error message

    $ python logging_level_example.py info
    INFO:root:This is an info message
    WARNING:root:This is a warning message
    ERROR:root:This is an error message
    CRITICAL:root:This is a critical error message

Naming Logger Instances
=======================

You will notice that these log messages all have 'root' embedded in them. The
logging module supports a hierarchy of loggers with different names. An easy
way to tell where a specific log message comes from is to use a separate
logger object for each of your modules. Each new logger "inherits" the
configuration of its parent, and log messages sent to a logger include the
name of that logger. Optionally, each logger can be configured differently, so
that messages from different modules are handled in different ways. Let's look
at a simple example of how to log from different modules so it is easy to
trace the source of the message:

.. include:: logging_modules_example.py
    :literal:
    :start-after: #end_pymotw_header


And the output:

::

    $ python logging_modules_example.py
    WARNING:package1.module1:This message comes from one module
    WARNING:package2.module2:And this message comes from another module

There are many, many, more options for configuring logging, including
different log message formatting options, having messages delivered to
multiple destinations, and changing the configuration of a long-running
application on the fly using a socket interface. All of these options are
covered in depth in the library module documentation.


.. seealso::

    `logging <http://docs.python.org/library/logging.html>`_
        The standard library documentation for this module.
