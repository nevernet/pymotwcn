###########################################
Implementing MapReduce with multiprocessing
###########################################

The Pool class can be used to create a simple single-server MapReduce implementation.  Although it does not give the full benefits of distributed processing, it does illustrate how easy it is to break some problems down into distributable units of work.

SimpleMapReduce
===============

In MapReduce, input data is broken down into chunks for processing by different worker instances.  Each chunk of input data is *mapped* to an intermediate state using a simple transformation.  The intermediate data is then collected together and partitioned based on a key value so that all of the related values are together.  Finally, the partitioned data is *reduced* to a result set.

.. include:: multiprocessing_mapreduce.py
    :literal:
    :start-after: #end_pymotw_header

Counting Words in Files
=======================

The following example script uses SimpleMapReduce to counts the "words" in the reStructuredText source for this article, ignoring some of the markup.  

.. include:: multiprocessing_wordcount.py
    :literal:
    :start-after: #end_pymotw_header

Each input filename is converted to a sequence of ``(word, 1)`` pairs by ``file_to_words``.  The data is partitioned by ``SimpleMapReduce.partition()`` using the word as the key, so the partitioned data consists of a key and a sequence of 1 values representing the number of occurrences of the word.  The reduction phase converts that to a pair of ``(word, count)`` values by calling ``count_words`` for each element of the partitioned data set.

.. {{{cog
.. cog.out(run_script(cog.inFile, 'multiprocessing_wordcount.py'))
.. }}}

::

	$ python multiprocessing_wordcount.py
	PoolWorker-1 reading communication.rst
	PoolWorker-1 reading mapreduce.rst
	
	TOP 20 WORDS BY FREQUENCY
	
	process         :    75
	multiprocessing :    40
	worker          :    34
	after           :    30
	running         :    29
	start           :    28
	processes       :    26
	python          :    26
	literal         :    25
	header          :    25
	pymotw          :    25
	end             :    25
	daemon          :    23
	now             :    21
	consumer        :    19
	starting        :    18
	exiting         :    16
	that            :    16
	event           :    15
	by              :    14

.. {{{end}}}

.. seealso::

    `MapReduce - Wikipedia <http://en.wikipedia.org/wiki/MapReduce>`_
        Overview of MapReduce on Wikipedia.
    
    `MapReduce: Simplified Data Processing on Large Clusters <http://labs.google.com/papers/mapreduce.html>`_
        Google Labs presentation and paper on MapReduce.


*Special thanks to Jesse Noller for helping review this information.*
