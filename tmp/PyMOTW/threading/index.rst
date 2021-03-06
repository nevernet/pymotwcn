=========
threading
=========
.. module:: threading
    :synopsis: Builds on the thread module to more easily manage several threads of execution.

:Module: threading
:Purpose: Builds on the thread module to more easily manage several threads of execution.
:Python Version: since 1.5.2 (some of these examples require 2.5 because they use the with statement)
:Abstract:

    The threading module lets you run multiple operations concurrently in the
    same process space.

Description
===========

The threading module builds on the low-level features of the thread module to
make working with threads even easier and more pythonic.

Thread objects
==============

The simplest way to use a thread is to instantiate it with a target function
and call start() to let it begin working.

::

    import threading

    def worker():
        """thread worker function"""
        print 'Worker'
        return

    threads = []
    for i in range(5):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()

The output, is unsurprisingly, 5 lines with "Worker" on each:

::

    $ python threading_simple.py
    Worker
    Worker
    Worker
    Worker
    Worker

It useful to be able to spawn a thread and pass it arguments to tell it what
work to do. For example, in PyMOTW: Queue, I created a simple program to
illustrate how to download enclosures from RSS/Atom feeds. Each downloader
thread needed to know where to find the URLs, and the Queue instance was
passed as an argument when the thread was created. Here, we'll just pass the
thread a number so the output is a little more interesting in the second
example.

::

    import threading

    def worker(num):
        """thread worker function"""
        print 'Worker:', num
        return

    threads = []
    for i in range(5):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

The integer argument is now included in the message printed by each thread:

::

    $ python threading_simpleargs.py
    Worker: 0
    Worker: 1
    Worker: 2
    Worker: 3
    Worker: 4

Determining the current thread
==============================

Using arguments to identify or name the thread is cumbersome, and unnecessary.
Each Thread instance has a name with a default value that you can change as
the thread is created. Naming threads is useful if you have a server process
with multiple service threads handling different operations. 

::

    import threading
    import time

    def worker():
        print threading.currentThread().getName(), 'Starting'
        time.sleep(2)
        print threading.currentThread().getName(), 'Exiting'

    def my_service():
        print threading.currentThread().getName(), 'Starting'
        time.sleep(3)
        print threading.currentThread().getName(), 'Exiting'

    t = threading.Thread(name='my_service', target=my_service)
    w = threading.Thread(name='worker', target=worker)
    w2 = threading.Thread(target=worker) # use default name

    w.start()
    w2.start()
    t.start()

The debug output includes the name of the current thread on each line. The
lines with "Thread-1" in the thread name column correspond to the unnamed
thread w2.

::

    $ python threading_names.py
    worker Starting
    Thread-1 Starting
    my_service Starting
    worker Exiting
    Thread-1 Exiting
    my_service Exiting

Of course, in most programs you won't use print to debug. The logging module
supports embedding the thread name in every log message using the formatter
code %(threadName)s. Including thread names in log messages makes it easier to
trace those messages back to their source.

::

    import logging
    import threading
    import time

    logging.basicConfig(level=logging.DEBUG,
                        format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                        )

    def worker():
        logging.debug('Starting')
        time.sleep(2)
        logging.debug('Exiting')

    def my_service():
        logging.debug('Starting')
        time.sleep(3)
        logging.debug('Exiting')

    t = threading.Thread(name='my_service', target=my_service)
    w = threading.Thread(name='worker', target=worker)
    w2 = threading.Thread(target=worker) # use default name

    w.start()
    w2.start()
    t.start()

The output from the format string above looks like:

::

    $ python threading_names_log.py
    [DEBUG] (worker    ) Starting
    [DEBUG] (Thread-1  ) Starting
    [DEBUG] (my_service) Starting
    [DEBUG] (worker    ) Exiting
    [DEBUG] (Thread-1  ) Exiting
    [DEBUG] (my_service) Exiting

Daemon vs. Non-Daemon Threads
=============================

Up until this point, I have been assuming that the main program does not exit
until all threads have completed their work. Sometimes you will want to spawn
a thread as a "daemon" that runs without blocking the main program from
exiting. Using daemon threads is useful for services where there may not be an
easy way to interrupt the thread or where letting the thread die in the middle
of its work does not lose or corrupt data (for example, a thread that
generates "heart beats" for a service monitoring tool). To mark a thread as a
daemon, call its setDaemon() with a boolean argument. The default is for
threads to not be daemons, so passing True turns the daemon mode on.

::

    import threading
    import time

    def daemon():
        print 'Starting:', threading.currentThread().getName()
        time.sleep(2)
        print 'Exiting :', threading.currentThread().getName()

    d = threading.Thread(name='daemon', target=daemon)
    d.setDaemon(True)

    def non_daemon():
        print 'Starting:', threading.currentThread().getName()
        print 'Exiting :', threading.currentThread().getName()

    t = threading.Thread(name='non-daemon', target=non_daemon)

    d.start()
    t.start()

Notice that the output does not include the "Exiting" message from the daemon
thread, since all of the non-daemon threads (including the main thread) exit
before the daemon thread wakes up from its 2 second sleep.

::

    $ python threading_daemon.py
    Starting: daemon
    Starting: non-daemon
    Exiting : non-daemon

To wait until the daemon thread has completed its work, use the join() method.

::

    import threading
    import time

    def daemon():
        print 'Starting:', threading.currentThread().getName()
        time.sleep(2)
        print 'Exiting :', threading.currentThread().getName()

    d = threading.Thread(name='daemon', target=daemon)
    d.setDaemon(True)

    def non_daemon():
        print 'Starting:', threading.currentThread().getName()
        print 'Exiting :', threading.currentThread().getName()

    t = threading.Thread(name='non-daemon', target=non_daemon)

    d.start()
    t.start()

    d.join()
    t.join()

Since we wait for the daemon thread to exit using join(), we do see its
"Exiting" message.

::

    $ python threading_daemon_join.py
    Starting: daemon
    Starting: non-daemon
    Exiting : non-daemon
    Exiting : daemon

By default, join() blocks indefinitely. It is also possible to pass a timeout
argument (a float representing the number of seconds to wait for the thread to
become inactive). If the thread does not complete within the timeout period,
join() returns anyway.

::

    import threading
    import time

    def daemon():
        print 'Starting:', threading.currentThread().getName()
        time.sleep(2)
        print 'Exiting :', threading.currentThread().getName()

    d = threading.Thread(name='daemon', target=daemon)
    d.setDaemon(True)

    def non_daemon():
        print 'Starting:', threading.currentThread().getName()
        print 'Exiting :', threading.currentThread().getName()

    t = threading.Thread(name='non-daemon', target=non_daemon)

    d.start()
    t.start()

    d.join(1)
    print 'd.isAlive()', d.isAlive()
    t.join()

Since the timeout passed is less than the amount of time the daemon thread
sleeps, the thread is still "alive" after join() returns.

::

    $ python threading_daemon_join_timeout.py
    Starting: daemon
    Starting: non-daemon
    Exiting : non-daemon
    d.isAlive() True

Using enumerate() to wait for all running threads
=================================================

It is not necessary to retain an explicit handle to all of the daemon threads
you start in order to ensure they have completed before exiting the main
process. threading.enumerate() returns a list of active Thread instances. The
list includes the current thread, and since joining the current thread is not
allowed (it introduces a deadlock situation), we must check before joining.

::

    import random
    import threading
    import time

    def worker():
        """thread worker function"""
        t = threading.currentThread()
        pause = random.randint(1,5)
        print 'Starting:', t.getName(), 'sleeping', pause
        time.sleep(pause)
        print 'Ending  :', t.getName()
        return

    for i in range(3):
        t = threading.Thread(target=worker)
        t.setDaemon(True)
        t.start()

    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is main_thread:
            continue
        print 'Joining :', t.getName()
        t.join()

Since the worker is sleeping for a random amount of time, your output may
vary. It should look something like this, though:

::

    $ python threading_enumerate.py
    Starting: Thread-1 sleeping 2
    Starting: Thread-2 sleeping 5
    Starting: Thread-3 sleeping 2
    Joining : Thread-1
    Ending  : Thread-1
    Joining : Thread-3
    Ending  : Thread-3
    Joining : Thread-2
    Ending  : Thread-2

Creating your own Thread class
==============================

When you start a Thread, it does some basic setup and then calls its run()
method, which calls the target function passed to the constructor. If you want
to create your own type of thread, you can subclass from Thread and override
run() to do whatever you want.

::

    import threading

    class MyThread(threading.Thread):

        def run(self):
            print 'MyThread:', self.getName()
            return

    for i in range(5):
        t = MyThread()
        t.start()

::

    $ python threading_subclass.py
    MyThread: Thread-1
    MyThread: Thread-2
    MyThread: Thread-3
    MyThread: Thread-4
    MyThread: Thread-5


Starting a task in a thread with a Timer
========================================

One example of a reason to subclass Thread is provided by Timer, also included
in threading. A Timer lets you start the work of your thread after a delay,
and cancel the operation at any point within that time period.

::

    import threading
    import time

    def delayed():
        print 'Worker running', threading.currentThread().getName()
        return

    t1 = threading.Timer(3, delayed)
    t1.setName('t1')
    t2 = threading.Timer(3, delayed)
    t2.setName('t2')

    print 'Starting timers'
    t1.start()
    t2.start()

    print 'Waiting before canceling', t2.getName()
    time.sleep(2)
    print 'Canceling', t2.getName()
    t2.cancel()
    print 'Main thread done'

Notice that the second timer is never run, and the first timer appears to run
after the rest of the main program is done. Since it is not a daemon thread,
we do not have to join() it explicitly to block waiting for it.

::

    $ python threading_timer.py
    Starting timers
    Waiting before canceling t2
    Canceling t2
    Main thread done
    Worker running t1

Signaling between threads with Event objects
============================================

Although the point of using multiple threads is to spin separate operations
off to run more or less simultaneously, there are times when it is important
to be able to synchronize the operations in two or more threads. A simple way
to communicate between threads is using Event objects. An Event manages an
internal flag that users can either set() or clear(). Other users can wait()
for the flag to be set(), effectively blocking progress until allowed to
continue. You can also think of an Event as a traffic light.

::

    import logging
    import threading
    import time

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s (%(threadName)-10s) %(message)s',
                        )
                        
    def wait_for_event(e):
        """Wait for the event to be set before doing anything"""
        logging.debug('wait_for_event starting')
        e.wait()
        logging.debug('e.isSet()->%s', e.isSet())

    def wait_for_event_timeout(e, t):
        """Wait t seconds and then timeout"""
        logging.debug('wait_for_event_timeout starting')
        e.wait(t)
        logging.debug('e.isSet()->%s', e.isSet())


    e = threading.Event()
    t1 = threading.Thread(name='block', 
                          target=wait_for_event,
                          args=(e,))
    t1.start()

    t2 = threading.Thread(name='non-block', 
                          target=wait_for_event_timeout, 
                          args=(e, 2))
    t2.start()

    logging.debug('Waiting before calling Event.set()')
    time.sleep(3)
    e.set()
    logging.debug('Event is set')


In this case, the non-block thread times out before the Event is set.

::

    $ python threading_event.py
    2008-01-13 13:25:02,514 (block     ) wait_for_event starting
    2008-01-13 13:25:02,525 (non-block ) wait_for_event_timeout starting
    2008-01-13 13:25:02,536 (MainThread) Waiting before calling Event.set()
    2008-01-13 13:25:04,526 (non-block ) e.isSet()->False
    2008-01-13 13:25:05,563 (MainThread) Event is set
    2008-01-13 13:25:05,564 (block     ) e.isSet()->True

Controlling access to resources with Lock
=========================================

In addition to synchronizing the operations of threads, it is also important
to be able to control access to shared resources to prevent corruption or
missed data. Python's built-in data structures (lists, dictionaries, etc.) are
thread-safe as a side-effect of having atomic byte-codes for manipulating them
(so the GIL is not released in the middle of an update). Your own data
structures implemented in Python (or simpler types like integers and floats),
don't have that protection. To guard against simultaneous access to an object,
use a Lock object.

::

    import logging
    import random
    import threading
    import time

    logging.basicConfig(level=logging.DEBUG,
                        format='(%(threadName)-10s) %(message)s',
                        )
                        
    class Counter(object):
        def __init__(self, start=0):
            self.lock = threading.Lock()
            self.value = start
        def increment(self):
            self.lock.acquire()
            try:
                logging.debug('Acquired lock')
                self.value = self.value + 1
            finally:
                self.lock.release()

    def worker(c):
        for i in range(3):
            pause = random.random()
            logging.debug('Sleeping %0.02f', pause)
            time.sleep(pause)
            c.increment()
        logging.debug('Done')

    counter = Counter()
    for i in range(5):
        t = threading.Thread(target=worker, args=(counter,))
        t.start()

    logging.debug('Waiting for worker threads')
    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()
    logging.debug('Counter: %d', counter.value)

In this example, the worker() function increments a Counter() instance. The
Counter manages a Lock to prevent two threads from changing its internal state
at the same time. If the Lock was not used, there is a possibility of missing
a change to the value attribute.

The random module is used to introduce variable sleep durations for each time
through the loop, so the output you see when running the sample code may vary.

::

    $ python threading_lock.py
    (Thread-1  ) Sleeping 0.66
    (Thread-2  ) Sleeping 0.83
    (Thread-3  ) Sleeping 0.41
    (Thread-4  ) Sleeping 0.32
    (Thread-5  ) Sleeping 0.77
    (MainThread) Waiting for worker threads
    (Thread-4  ) Acquired lock
    (Thread-4  ) Sleeping 0.54
    (Thread-3  ) Acquired lock
    (Thread-3  ) Sleeping 0.18
    (Thread-3  ) Acquired lock
    (Thread-3  ) Sleeping 0.02
    (Thread-3  ) Acquired lock
    (Thread-3  ) Done
    (Thread-1  ) Acquired lock
    (Thread-1  ) Sleeping 0.22
    (Thread-5  ) Acquired lock
    (Thread-5  ) Sleeping 0.34
    (Thread-2  ) Acquired lock
    (Thread-2  ) Sleeping 0.51
    (Thread-1  ) Acquired lock
    (Thread-1  ) Sleeping 0.03
    (Thread-4  ) Acquired lock
    (Thread-4  ) Sleeping 0.26
    (Thread-1  ) Acquired lock
    (Thread-1  ) Done
    (Thread-4  ) Acquired lock
    (Thread-4  ) Done
    (Thread-5  ) Acquired lock
    (Thread-5  ) Sleeping 0.02
    (Thread-5  ) Acquired lock
    (Thread-5  ) Done
    (Thread-2  ) Acquired lock
    (Thread-2  ) Sleeping 0.17
    (Thread-2  ) Acquired lock
    (Thread-2  ) Done
    (MainThread) Counter: 15

If another thread has acquired the lock, it might be preferable to find that
out without blocking all action in the current thread. In that case, pass a
False value for the blocking argument to acquire(). In the next example,
worker() tries to acquire the lock 3 separate times, and counts how many
attempts it has to make to do so. The random sleeps are used to simulate
varying load in the different threads.

::

    import logging
    import random
    import threading
    import time

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s (%(threadName)-8s) %(message)s',
                        )
                        
    def random_pause():
        pause = random.random()
        time.sleep(pause)                
                        
    def worker(lock):
        logging.debug('Starting')
        num_tries = 0
        num_acquires = 0
        while num_acquires < 3:
            random_pause()
            have_it = lock.acquire(0)
            try:
                num_tries += 1
                if have_it:
                    logging.debug('Iteration %d: Acquired',  num_tries)
                    num_acquires += 1
                    random_pause()
                else:
                    logging.debug('Iteration %d: Not acquired', num_tries)
            finally:
                if have_it:
                    lock.release()
        logging.debug('Done after %d iterations', num_tries)

    lock = threading.Lock()
    for i in range(3):
        t = threading.Thread(target=worker, args=(lock,))
        t.start()

As you can see, it takes some of the threads many more than 3 iterations to
acquire the lock 3 separate times.

::

    $ python threading_lock_noblock.py
    2008-01-13 14:48:27,712 (Thread-1) Starting
    2008-01-13 14:48:27,723 (Thread-2) Starting
    2008-01-13 14:48:27,735 (Thread-3) Starting
    2008-01-13 14:48:28,173 (Thread-1) Iteration 1: Acquired
    2008-01-13 14:48:28,624 (Thread-2) Iteration 1: Acquired
    2008-01-13 14:48:28,674 (Thread-3) Iteration 1: Not acquired
    2008-01-13 14:48:28,861 (Thread-1) Iteration 2: Not acquired
    2008-01-13 14:48:29,314 (Thread-2) Iteration 2: Acquired
    2008-01-13 14:48:29,653 (Thread-3) Iteration 2: Not acquired
    2008-01-13 14:48:29,674 (Thread-1) Iteration 3: Not acquired
    2008-01-13 14:48:29,986 (Thread-1) Iteration 4: Not acquired
    2008-01-13 14:48:30,003 (Thread-1) Iteration 5: Not acquired
    2008-01-13 14:48:30,067 (Thread-3) Iteration 3: Not acquired
    2008-01-13 14:48:30,543 (Thread-2) Iteration 3: Acquired
    2008-01-13 14:48:30,605 (Thread-2) Done after 3 iterations
    2008-01-13 14:48:30,639 (Thread-3) Iteration 4: Acquired
    2008-01-13 14:48:30,755 (Thread-1) Iteration 6: Not acquired
    2008-01-13 14:48:31,069 (Thread-1) Iteration 7: Acquired
    2008-01-13 14:48:31,943 (Thread-3) Iteration 5: Not acquired
    2008-01-13 14:48:32,654 (Thread-3) Iteration 6: Acquired
    2008-01-13 14:48:32,949 (Thread-1) Iteration 8: Not acquired
    2008-01-13 14:48:33,693 (Thread-1) Iteration 9: Acquired
    2008-01-13 14:48:33,812 (Thread-1) Done after 9 iterations
    2008-01-13 14:48:34,336 (Thread-3) Iteration 7: Acquired
    2008-01-13 14:48:35,003 (Thread-3) Done after 7 iterations

Re-entrant Locks
================

Normal Lock objects cannot be acquired more than once, even by the same
thread. This can introduce undesirable side-effects if a lock is accessed by
more than one function in the same call chain.

::

    import threading

    lock = threading.Lock()

    def first():
        print 'First try:', lock.acquire()
        second()
        
    def second():
        print 'Second try:', lock.acquire(0)

    first()

In this case, since both functions are using the same global lock, and one
calls the other, the second acquisition fails and would have blocked if we did
not tell acquire() not to block.

::

    $ python threading_lock_reacquire.py
    First try: True
    Second try: False

In a situation where separate code from the same thread needs to "re-acquire"
the lock, use an RLock instead.

::

    import threading

    lock = threading.RLock()

    def first():
        print 'First try:', lock.acquire()
        second()
        
    def second():
        print 'Second try:', lock.acquire(0)

    first()

The only change to the code from the previous example was substituting RLock
for Lock.

::

    $ python threading_rlock.py
    First try: True
    Second try: 1

Locks and with
==============

Locks are also compatible with new with statement, introduced in __future__
for Python 2.5 and part of the language for 2.6. Using with removes the need
to explicitly acquire and release the lock.

::

    from __future__ import with_statement
    import threading

    def worker_with(lock):
        with lock:
            print 'Lock acquired via with'
            
    def worker_no_with(lock):
        lock.acquire()
        try:
            print 'Lock acquired directly'
        finally:
            lock.release()

    lock = threading.Lock()
    w = threading.Thread(target=worker_with, args=(lock,))
    nw = threading.Thread(target=worker_no_with, args=(lock,))

    w.start()
    nw.start()

The two functions worker_with() and worker_no_with() manage the lock in
equivalent ways.

::

    $ python threading_lock_with.py
    Lock acquired via with
    Lock acquired directly

Synchronizing threads with a Condition object
=============================================

In addition to using Events, another way of synchronizing threads is through
using a Condition object. Because the Condition uses a Lock, it can be tied to
a shared resource. This allows threads to wait for the resource to be updated.
In this example, the consumer() threads wait() for the Condition to be set
before continuing. The producer() thread is responsible for setting the
condition and notifying the other threads once they can continue.

::

    from __future__ import with_statement
    import logging
    import threading
    import time

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s (%(threadName)-2s) %(message)s',
                        )

    def consumer(cond):
        """wait for the condition and use the resource"""
        logging.debug('Starting consumer thread')
        t = threading.currentThread()
        with cond:
            cond.wait()
            logging.debug('Resource is available to consumer')

    def producer(cond):
        """set up the resource to be used by the consumer"""
        logging.debug('Starting producer thread')
        with cond:
            logging.debug('Making resource available')
            cond.notifyAll()

    condition = threading.Condition()
    c1 = threading.Thread(name='c1', target=consumer, args=(condition,))
    c2 = threading.Thread(name='c2', target=consumer, args=(condition,))
    p = threading.Thread(name='p', target=producer, args=(condition,))

    c1.start()
    time.sleep(2)
    c2.start()
    time.sleep(2)
    p.start()

The threads use with to acquire the lock associated with the Condition. You
can also call the acquire() and release() methods explicitly, if you are not
using Python 2.5.

::

    $ python threading_condition.py
    2008-01-13 13:01:24,226 (c1) Starting consumer thread
    2008-01-13 13:01:26,238 (c2) Starting consumer thread
    2008-01-13 13:01:28,248 (p ) Starting producer thread
    2008-01-13 13:01:28,249 (p ) Making resource available
    2008-01-13 13:01:28,249 (c1) Resource is available to consumer
    2008-01-13 13:01:28,250 (c2) Resource is available to consumer

Controlling concurrent access to resources with a Semaphore
===========================================================

Sometimes it is useful to allow more than one access to a resource at a time,
while still limiting the overall number. For example, a connection pool might
support a fixed number of simultaneous connections, or a network application
might support a fixed number of concurrent downloads. A Semaphore is one way
to manage those connections.

::

    from __future__ import with_statement
    import logging
    import random
    import threading
    import time

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s (%(threadName)-2s) %(message)s',
                        )

    class ActivePool(object):
        def __init__(self):
            super(ActivePool, self).__init__()
            self.active = []
            self.lock = threading.Lock()
        def makeActive(self, name):
            with self.lock:
                self.active.append(name)
        def makeInactive(self, name):
            with self.lock:
                self.active.remove(name)
        def __str__(self):
            with self.lock:
                return str(self.active)

    def worker(s, pool):
        with s:
            name = threading.currentThread().getName()
            pool.makeActive(name)
            logging.debug('Running: %s', str(pool))
            time.sleep(random.random())
            pool.makeInactive(name)

    pool = ActivePool()
    s = threading.Semaphore(5)
    for i in range(20):
        t = threading.Thread(target=worker, name=str(i), args=(s, pool))
        t.start()

In this example, the ActivePool class simply serves as a convenient way to
track which threads are able to run at a given moment. A real resource pool
would probably allocate a connection or some other value to the newly active
thread, and reclaim the value when the thread is done. Here it is just used to
hold the names of the active threads to show that only 5 are running
concurrently.

::

    $ python threading_semaphore.py
    2008-01-13 15:35:06,562 (0 ) Running: ['0']
    2008-01-13 15:35:06,573 (1 ) Running: ['0', '1']
    2008-01-13 15:35:06,584 (2 ) Running: ['0', '1', '2']
    2008-01-13 15:35:06,596 (3 ) Running: ['1', '2', '3']
    2008-01-13 15:35:06,607 (4 ) Running: ['1', '2', '3', '4']
    2008-01-13 15:35:06,619 (5 ) Running: ['1', '2', '3', '4', '5']
    2008-01-13 15:35:06,671 (6 ) Running: ['1', '3', '4', '5', '6']
    2008-01-13 15:35:06,729 (7 ) Running: ['1', '3', '4', '5', '7']
    2008-01-13 15:35:07,139 (8 ) Running: ['1', '3', '4', '7', '8']
    2008-01-13 15:35:07,502 (9 ) Running: ['1', '3', '4', '7', '9']
    2008-01-13 15:35:07,564 (10) Running: ['3', '4', '7', '9', '10']
    2008-01-13 15:35:07,566 (11) Running: ['9', '10', '11']
    2008-01-13 15:35:07,566 (12) Running: ['9', '10', '11', '12']
    2008-01-13 15:35:07,567 (13) Running: ['9', '10', '11', '12', '13']
    2008-01-13 15:35:07,683 (14) Running: ['9', '11', '12', '13', '14']
    2008-01-13 15:35:08,055 (15) Running: ['11', '12', '13', '14', '15']
    2008-01-13 15:35:08,149 (16) Running: ['12', '13', '14', '15', '16']
    2008-01-13 15:35:08,150 (17) Running: ['12', '13', '15', '16', '17']
    2008-01-13 15:35:08,319 (18) Running: ['12', '13', '16', '17', '18']
    2008-01-13 15:35:08,531 (19) Running: ['12', '16', '17', '18', '19']

Keeping thread-specific data with local
=======================================

While some resources need to be locked so multiple threads can use them,
others need to be protected so that they are hidden from view in threads that
do not "own" them. The threading.local() creates an object capable of hiding
values from view in separate threads.

::

    import random
    import threading

    def show_value(data):
        print threading.currentThread().getName(), ': value=',
        try:
            print data.value
        except AttributeError:
            print 'No value yet'

    def worker(data):
        show_value(data)
        data.value = random.randint(1, 100)
        show_value(data)

    local_data = threading.local()
    show_value(local_data)
    local_data.value = 1000
    show_value(local_data)

    for i in range(2):
        t = threading.Thread(target=worker, args=(local_data,))
        t.start()

Notice that local_data.value is not present for any thread until it is set in
that thread.

::

    $ python threading_local.py
    MainThread : value= No value yet
    MainThread : value= 1000
    Thread-1 : value= No value yet
    Thread-1 : value= 19
    Thread-2 : value= No value yet
    Thread-2 : value= 26

To initialize the settings so all threads start with the same value, use a
subclass and set the attributes in __init__().

::

    import random
    import threading

    def show_value(data):
        print threading.currentThread().getName(), ': value=',
        try:
            print data.value
        except AttributeError:
            print 'No value yet'

    def worker(data):
        show_value(data)
        data.value = random.randint(1, 100)
        show_value(data)

    class MyLocal(threading.local):
        def __init__(self, value):
            print '(Initializing %s for %s)' % (id(self), threading.currentThread().getName()),
            self.value = value

    local_data = MyLocal(1000)
    show_value(local_data)

    for i in range(2):
        t = threading.Thread(target=worker, args=(local_data,))
        t.start()

The output shows that __init__() is invoked on the same object (note the id()
value), once in each thread.

::

    $ python threading_local_defaults.py
    (Initializing 479616 for MainThread) MainThread : value= 1000
    Thread-1 : value= (Initializing 479616 for Thread-1) 1000
    Thread-1 : value= 79
    Thread-2 : value= (Initializing 479616 for Thread-2) 1000
    Thread-2 : value= 56


