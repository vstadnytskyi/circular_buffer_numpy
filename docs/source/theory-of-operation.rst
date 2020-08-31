===================
Theory of Operation
===================

------------
Introduction
------------

Buffers are widely used in the computer architecture to allow efficient data storage, handling and later retrieval.

This project uses numpy array data structures to provide a fast and flexible data handling for streams of data. It is common to have a data acquisition unit that measures at a certain rate. The data from the internal buffer need to be read efficiently and should be available to other programs\devices at later time. The numpy array data structure in Python allows to preallocate memory at the initialization and the data handling from now on is extremely efficient.

Queue
-----

Queue is an abstract data type where data is maintained in a sequence and can be modified by addition and removal of the entries. By convention, the end of the sequence at which elements are added is called the back, tail, or rear of the queue, and the end at which elements are removed is called the head or front of the queue, analogously to the words used when people line up to wait for goods or services. (read more https://en.wikipedia.org/wiki/Queue_(abstract_data_type)). The implementation of the Queue in this library uses underlying numpy array structure to insure fast and reliable data addition and removal from the queue.

Definitions
^^^^^^^^^^^^^^^^^^^^^^^^^^
In this section, we describe definitions of variables and their meaning.

* 'rear' is a pointer at current next available cell to enqueue.

* 'length' the number of entries in the queue.

* 'data_shape' - the shape of the one data entry.

* 'shape' - shape of the entire available queue space.

Circular Buffer
---------------


Shape
-----

The shape of the circular buffer and queue objects follows the numpy convention. The first element in the shape (fast axis) defines the circular length of the buffer and the rest define the dimensionality of the data stored.

Example:
the shape circular buffer with the shape = (100,2,2) has the length of 100 and datapoint_shape of (2,2)

Design Specification
------------------------
DI-4108 by DATAQ in 4kHz at 8 analog channels at 16bit resolution plus 1 digital channel will produce 68kB of data per second.



Benchmarks
------------------------
Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^

:OS: macOS Mojave 10.14.6
:Computer: MacBook Pro (13-inch, 2017, Two Thunderbolt 3 ports)
:Processor: 2.3 GHz Intel Core i5
:Memory: 16 GB 2133 MHz LPDDR3


Write/Read time benchmarks
^^^^^^^^^^^^^^^^^^^^^^^^^^


.. figure::  write-benchmarks-0.0.6.jpg
   :align:   center


.. figure::  read-benchmarks-0.0.6.jpg
   :align:   center

The numerical output :: python
   >>> python3 examples/write-read\ benchmarks.py
     circular buffer numpy version: 0.0.6
     1.875741365999999e-06 per write and 1.3417917090000007e-06 per read of 1x10 array
     1.4111644630000003e-05 per write and 1.3084426500000036e-06 per read of 10x10 array
     0.00012056339729999994 per write and 1.2482045999998803e-06 per read of 100x10 array
     0.001347408767000001 per write and 1.2678269999994995e-06 per read of 1000x10 array
     0.01340139582999999 per write and 1.9024200000217206e-06 per read of 10000x10 array
     2.005417302999998e-06 per write and 1.324801278999999e-06 per read of 1x100 array
     1.650482488999998e-05 per write and 1.2904178099999797e-06 per read of 10x100 array
     0.00013166361600000016 per write and 1.2773896999998869e-06 per read of 100x100 array
     0.0012954091400000003 per write and 1.2730259999997885e-06 per read of 1000x100 array
     0.013044410029999974 per write and 1.377e-06 per read of 10000x100 array
     1.2233516567000002e-05 per write and 1.455e-06 per read of 1x1000 array
     0.00014691199192 per write and 1.2784705600000024e-06 per read of 10x1000 array
     0.001376928726700001 per write and 1.3089801000006674e-06 per read of 100x1000 array
     0.012413041053 per write and 1.5748430000002146e-06 per read of 1000x1000 array
     0.12879166736000003 per write and 8.44166999996787e-06 per read of 10000x1000 array
