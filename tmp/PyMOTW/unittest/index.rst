========
unittest
========
.. module:: unittest
    :synopsis: Automated testing framework

:Module: unittest
:Purpose: Automated testing framework
:Python Version: 2.1

Description
===========

Python's unittest module, sometimes referred to as PyUnit, is based on the
XUnit framework design by Kent Beck and Erich Gamma. The same pattern is
repeated in many other languages, including C, perl, Java, and Smalltalk. The
framework implemented by unittest supports fixtures, test suites, and a test
runner to enable automated testing for your code.

Basic Test Structure
====================

Tests, as defined by the unittest module, have two parts: code to manage test
"fixtures", and the test itself. Individual tests are created by subclassing
unittest.TestCase and overriding or adding appropriate methods. For example,

::

    import unittest

    class SimplisticTest(unittest.TestCase):
        def test(self):
            self.failUnless(True)

    if __name__ == '__main__':
        unittest.main()

In this case, the SimplisticTest has a single test() method, which would fail
if True is ever False. 

Running Tests
=============

The simplest way to run unittest tests is to include:

::

    if __name__ == '__main__':
        unittest.main()

at the bottom of each test file, then simply run the script directly from the
command line:

::

    $ python unittest_simple.py
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.000s

    OK

This abbreviated output includes the amount of time the tests took, along with
a status indicator for each test (the "." on the first line of output means
that a test passed). For more detailed test results, include the -v option:

::

    $ python unittest_simple.py -v
    test (__main__.SimplisticTest) ... ok

    ----------------------------------------------------------------------
    Ran 1 test in 0.001s

    OK

Test Outcomes
=============

Tests have 3 possible outcomes:

::

    ok
    The test passes.
    FAIL
    The test does not pass, and raises an AssertionError exception.
    ERROR
    The test raises an exception other than AssertionError.

There is no explicit way to cause a test to "pass", so a test's status depends
on the presence (or absence) of an exception. 

::

    class OutcomesTest(unittest.TestCase):

        def testPass(self):
            return

        def testFail(self):
            self.failIf(True)

        def testError(self):
            raise RuntimeError('Test error!')

When a test fails or generates an error, the traceback is included in the
output.

::

    $ python unittest_outcomes.py   
    EF.
    ======================================================================
    ERROR: testError (__main__.OutcomesTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "unittest_outcomes.py", line 43, in testError
        raise RuntimeError('Test error!')
    RuntimeError: Test error!

    ======================================================================
    FAIL: testFail (__main__.OutcomesTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "unittest_outcomes.py", line 40, in testFail
        self.failIf(True)
    AssertionError

    ----------------------------------------------------------------------
    Ran 3 tests in 0.002s

    FAILED (failures=1, errors=1)


In the example above, testFail() fails and the traceback shows the line with
the failure code. It is up to the person reading the test output to look at
the code to figure out the semantic meaning of the failed test, though. To
make it easier to understand the nature of a test failure, the fail*() and
assert*() methods all accept an argument msg, which can be used to produce a
more detailed error message.

::

    class FailureMessageTest(unittest.TestCase):
        def testFail(self):
            self.failIf(True, 'failure message goes here')

::

    $ python unittest_failwithmessage.py -vtestFail (__main__.FailureMessageTest) ... FAIL

    ======================================================================
    FAIL: testFail (__main__.FailureMessageTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "unittest_failwithmessage.py", line 37, in testFail
        self.failIf(True, 'failure message goes here')
    AssertionError: failure message goes here

    ----------------------------------------------------------------------
    Ran 1 test in 0.002s

    FAILED (failures=1)


Asserting Truth
===============

Most tests assert the truth of some condition. There are a few different ways
to write truth-checking tests, depending on the perspective of the test author
and the desired outcome of the code being tested. If the code produces a value
which can be evaluated as true, the methods failUnless() and assertTrue()
should be used. If the code produces a false value, the methods failIf() and
assertFalse() make more sense. 

::

    class TruthTest(unittest.TestCase):

        def testFailUnless(self):
            self.failUnless(True)

        def testAssertTrue(self):
            self.assertTrue(True)

        def testFailIf(self):
            self.failIf(False)

        def testAssertFalse(self):
            self.assertFalse(False)


Testing Equality
================

As a special case, unittest includes methods for testing the equality of two
values. 

::

    class EqualityTest(unittest.TestCase):

        def testEqual(self):
            self.failUnlessEqual(1, 3-2)

        def testNotEqual(self):
            self.failIfEqual(2, 3-2)


These special tests are handy, since the values being compared appear in the
failure message when a test fails.

::

    class InequalityTest(unittest.TestCase):

        def testEqual(self):
            self.failIfEqual(1, 3-2)

        def testNotEqual(self):
            self.failUnlessEqual(2, 3-2)


And when these tests are run:

::

    $ python unittest_notequal.py -v
    testEqual (__main__.EqualityTest) ... FAIL
    testNotEqual (__main__.EqualityTest) ... FAIL

    ======================================================================
    FAIL: testEqual (__main__.EqualityTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "unittest_notequal.py", line 37, in testEqual
        self.failIfEqual(1, 3-2)
    AssertionError: 1 == 1

    ======================================================================
    FAIL: testNotEqual (__main__.EqualityTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "unittest_notequal.py", line 40, in testNotEqual
        self.failUnlessEqual(2, 3-2)
    AssertionError: 2 != 1

    ----------------------------------------------------------------------
    Ran 2 tests in 0.002s

    FAILED (failures=2)


Almost Equal?
=============

In addition to strict equality, it is possible to test for near equality of
floating point numbers using failIfAlmostEqual() and failUnlessAlmostEqual().

::

    class AlmostEqualTest(unittest.TestCase):

        def testNotAlmostEqual(self):
            self.failIfAlmostEqual(1.1, 3.3-2.0, places=1)

        def testAlmostEqual(self):
            self.failUnlessAlmostEqual(1.1, 3.3-2.0, places=0)

The arguments are the 2 values to be compared, and the number of decimal
places to use for the test.

::

    $ python  unittest_almostequal.py   
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.001s

    OK


Testing for Exceptions
======================

As previously mentioned, if a test raises an exception it is treated as an
error in the test. This is very useful for uncovering mistakes while you are
modifying code which has existing test coverage. There are circumstances,
however, in which you want the test to verify that some code does produce an
exception. For example, if an invalid value is given to an attribute of an
object. In such cases, TestCase.failUnlessRaises() makes the code more clear
than trapping the exception yourself. Compare these two tests:

::

    def raises_error(*args, **kwds):
        print args, kwds
        raise ValueError('Invalid value: ' + str(args) + str(kwds))

    class ExceptionTest(unittest.TestCase):

        def testTrapLocally(self):
            try:
                raises_error('a', b='c')
            except ValueError:
                pass
            else:
                self.fail('Did not see ValueError')

        def testFailUnlessRaises(self):
            self.failUnlessRaises(ValueError, raises_error, 'a', b='c')

The results for both are the same, but the second test using
failUnlessRaises() is more succinct.

::

    $ python unittest_exception.py -v
    testFailUnlessRaises (__main__.ExceptionTest) ... ('a',) {'b': 'c'}
    ok
    testTrapLocally (__main__.ExceptionTest) ... ('a',) {'b': 'c'}
    ok

    ----------------------------------------------------------------------
    Ran 2 tests in 0.001s

    OK


Test Fixtures
=============

Fixtures are resources needed by a test. For example, if you are writing
several tests for the same class, those tests all need an instance of that
class to use for testing. Other test fixtures include database connections and
temporary files (many people would argue that using external resources makes
such tests not "unit" tests, but they are still tests and still useful).
TestCase includes a special hook to configure and clean up any fixtures needed
by your tests. To configure the fixtures, override setUp(). To clean up,
override tearDown().

::

    class FixturesTest(unittest.TestCase):

        def setUp(self):
            print 'In setUp()'
            self.fixture = range(1, 10)

        def tearDown(self):
            print 'In tearDown()'
            del self.fixture

        def test(self):
            print 'in test()'
            self.failUnlessEqual(self.fixture, range(1, 10))

When this sample test is run, you can see the order of execution of the
fixture and test methods:

::

    $ python unittest_fixtures.py 
    In setUp()
    in test()
    In tearDown()
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.001s

    OK


Test Suites
===========

The standard library documentation describes how to organize test suites
manually. I generally do not use test suites directly, because I prefer to
build the suites automatically (these are automated tests, after all).
Automating the construction of test suites is especially useful for large code
bases, in which related tests are not all in the same place. Tools such as
nose and Proctor make it easier to manage tests when they are spread over
multiple files and directories.


