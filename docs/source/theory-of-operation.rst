===================
Theory of Operation
===================

Introduction
------------
Buffers are widely used in the computer architecture to allow efficient data storage, handling and later retrieval.

This project uses numpy array data structures to provide a fast and flexible data handling for streams of data. It is common to have a data acquisition unit that measures at a certain rate. The data from the internal buffer need to be read efficiently and should be available to other programs\devices at later time. The numpy array data structure in Python allows to preallocate memory at the initialization and the data handling from now on is extremely efficient.

Design Specification
--------------------

Benchmarks
----------
Configuration:
DI-4108 by DATAQ in 4kHz at 8 analog channels at 16bit resolution plus 1 digital channel will produce 68kB of data per second.

TODO write a test to measure write/read time
write time:

read time:
