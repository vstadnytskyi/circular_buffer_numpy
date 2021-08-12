=====
Usage
=====

In this section you will:

* Learn how to create your first circular buffer and perform simple operations with it.
* Learn how to create your first queue buffer and perform simple operations with it.
* Learn few example on when to use circular buffer and when to use queue.

The Circular Buffer
-------------------------

The circular buffer is a data structure that allows you to allocate part of memory to store data, quickly append data and retrieve data. Remember that the circular buffer has limited "length" and the data is overwritten when you append more data than it can hold. The naming of the buffer class properties are taken from numpy array names, hence it should be familiar to numpy array users.

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

First, let us create a test numpy array with the shape corresponding to "data_shape" of the buffer. Let us make a vector of length two and populate it with two values: current time and a random number. These two numbers represent one 2D  data point (number vs time). Remember! the data point in this circular buffer can be a numpy array on its' own.

.. code-block:: python

    In [7]: from numpy import empty, random
    In [8]: from time import time
    In [9]: data_point = empty(shape = buffer.data_shape)
    In [10]: data_point[0] = time()
    In [11]: data_point[1] = random.randint(0,4096)

The "data_point" represents a typical single data entry acquired from a data acquisition device. This data can be now appened to the circular buffer. We can examine the location of the last known entry in the buffer, which is "0" in our case since we added only one data point.

.. code-block:: python

    In [12]: buffer.append(arr)
    In [13]: buffer.pointer
    Out[13]: 0
    In [14]: for i in range(10):
                data_point[0] = time()
                data_point[1] = random.randint(0,4096)
                buffer.append(data_point)

Next, we can examine the content of the circular buffer. There are several build in methods to get data from the buffer.

* "get_data()" - returns all valid data in the buffer.
* "get_last_N(N=5)" - returns last N entries in the circular buffer
* "get_last_value()" - returns the very last known entry in the circular buffer

.. code-block:: python

    In [15]: buffer.get_data()
    Out[15]:
    array([[1.61452783e+09, 4.07500000e+03],
           [1.61452783e+09, 1.00600000e+03],
           [1.61452788e+09, 2.01400000e+03],
           [1.61452788e+09, 2.02300000e+03],
           [1.61452788e+09, 2.83000000e+03],
           [1.61452788e+09, 7.12000000e+02],
           [1.61452788e+09, 1.31900000e+03],
           [1.61452788e+09, 1.40500000e+03],
           [1.61452788e+09, 3.41600000e+03],
           [1.61452788e+09, 2.27000000e+02],
           [1.61452788e+09, 2.59000000e+02],
           [1.61452788e+09, 3.69000000e+03]])

     In [16]: buffer.get_last_N(5)
     Out[16]:
     array([[1.61452788e+09, 1.40500000e+03],
            [1.61452788e+09, 3.41600000e+03],
            [1.61452788e+09, 2.27000000e+02],
            [1.61452788e+09, 2.59000000e+02],
            [1.61452788e+09, 3.69000000e+03]])

      In [17]: buffer.get_last_value()
      Out[17]: array([[1.61452788e+09, 3.69000000e+03]])

The Queue Class
---------------

The queue class has very similar functionality to the circular buffer class with few modifications. The valid entry in the queue can be read only once, when you retrieve the data from the queue, it is not available anymore. The class mimics performance of first in first out(FIFO) buffer.

.. code-block:: python

  In [1]: from circular_buffer_numpy.queue import Queue
  In [2]: queue = Queue(shape = (100,2), dtype = 'float64')

Now, we have an instance of the Queue class named "queue". Let us explore inner properties of the queue.

  * "shape" - total shape of the underlying numpy array
  * "length" - number of entried in the queue.
  * "data_shape" - size of the individual data point.
  * "rear" - the index in the underlying numpy array pointing at the next empty slot in the queue.
  * "global_rear" - the global index showing how many data points have been enqueued since the creation of the instance.

  .. code-block:: python


  In [3]: queue.length
  Out[3]: 0

  In [4]: queue.shape
  Out[4]: (100, 2)

  In [5]: queue.data_shape
  Out[5]: (2,)

  In [6]: queue.rear
  Out[6]: 0

  In [7]: queue.global_rear
  Out[7]: 0


The "data_point" represents a typical single data entry acquired from a data acquisition device. This data can be now appended to the circular buffer. We can examine the location of the last known entry in the buffer, which is "0" in our case since we added only one data point.
