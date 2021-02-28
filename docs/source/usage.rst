=====
Usage
=====

In this section you will:

* Learn how to create your first circular buffer and perform simple operations with it.
* Learn how to create your first queue buffer and perform simple operations with it.
* Learn few example on when to use circular buffer and when to use queue.

The Circular Buffer
-------------------------

The circular buffer is a data structure that allows you to allocate part of memory to store data, quickly append data and retrieve data. Remember that the circular buffer has limited "length" and the data is overwritten when you append more data than it can hold.

First, let us import the "CircularBuffer" class and create our first circular buffer. In the example below, we create a circular buffer with "shape" 100 by 2, and 'float64' as type of stored data. The length of the buffer is 100 and each entry holds 2 values, for example (time, temperature).

.. code-block:: python

    In [1]: from circular_buffer_numpy.circular_buffer import CircularBuffer

    In [2]: buffer = CircularBuffer(shape = (100,2), dtype = 'float64')

Now, we have an instance of circular buffer named buffer. Let us explore inner properties of the buffer.

* "shape" - total shape of the underlying numpy array
* "length" - length of the buffer.
* "data_shape" - size of the individual data point.
* "pointer" - last known entry in the buffer. the very first value is "-1"

.. code-block:: python

    In [3]: buffer.shape
    Out[3]: (100, 2)

    In [4]: buffer.length
    Out[4]: 100

    In [5]: buffer.data_shape
    Out[5]: (2,)

    In [6]: buffer.pointer
    Out[6]: -1

Now, we have an instance of circular buffer named buffer and we know something about. Let us explore different operation that can be performed with the buffer.

First, let us create a empty array with

.. code-block:: python

    In [7]: from numpy import empty, random
    In [8]: from time import time
    In [9]: arr = empty(shape = buffer.data_shape)
    In [10]: arr[0] = time()
    In [11]: arr[1] = random.randint(0,4096)

First, let us create

.. code-block:: python
    In [12]: buffer.append(arr)
    In [14]: buffer.pointer
    Out[15]: 9

    In [16]: buffer.get_last_value()
    Out[16]:
    array([[[[0., 0., 0., 0.],
             [0., 0., 0., 0.],
             [0., 0., 0., 0.]],

            [[0., 0., 0., 0.],
             [0., 0., 0., 0.],
             [0., 0., 0., 0.]]]])

The Queue Class
---------------

.. code-block:: python

  import queue
