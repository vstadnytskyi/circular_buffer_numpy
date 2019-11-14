=====
Usage
=====

Start by importing Numpy array circular buffer.

The Circular Buffer Class
-------------------------

.. code-block:: python

    In [1]: from circular_buffer_numpy.circular_buffer import CircularBuffer

    In [2]: buffer = CircularBuffer(shape = (100,2,3,4), dtype = 'float64')

    In [3]: buffer.shape
    Out[3]: (100, 2, 3, 4)

    In [4]: buffer.length
    Out[4]: 100

    In [5]: buffer.data_shape
    Out[5]: (2, 3, 4)

    In [6]: buffer.pointer
    Out[6]: -1

    In [7]: from numpy import zeros
    In [8]: arr = zeros((10,2,3,4))
    In [9]: buffer.append(arr)
    In [10]: buffer.pointer
    Out[10]: 9

    In [11]: buffer.get_last_value()
    Out[11]:
    array([[[[0., 0., 0., 0.],
             [0., 0., 0., 0.],
             [0., 0., 0., 0.]],

            [[0., 0., 0., 0.],
             [0., 0., 0., 0.],
             [0., 0., 0., 0.]]]])

.. autoclass:: circular_buffer_numpy.circular_buffer.CircularBuffer
  :members:

The Queue Class
---------------

.. code-block:: python

  import queue

.. autoclass:: circular_buffer_numpy.queue.Queue
  :members:
