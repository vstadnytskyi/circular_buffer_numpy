#!/bin/env python
# -*- coding: utf-8 -*-
"""Queue
    by Valentyn Stadnytskyi
    created: Nov 4, 2017
    last update: February, 2019
Queue is an abstract data structure, somewhat similar to Stacks. Unlike stacks, a queue is open at both its ends.
One end is always used to insert data (enqueue) and the other is used to remove data (dequeue).
Basic Operations
Queue operations may involve initializing or defining the queue,
utilizing it, and then completely erasing it from the memory.
Here we shall try to understand the basic operations associated with queues −
enqueue() − add (store) an item to the queue.
dequeue() − remove (access) an item from the queue.
Few more functions are required to make the above-mentioned queue operation efficient. These are −
peek() − Gets the element at the front of the queue without removing it. isfull() − Checks if the queue is full.
isempty() − Checks if the queue is empty.
"""

from logging import debug, info, warn, error
debug('importing queue')
class Queue(object):
    """
    queue data structure implemented using numpy arrays.

    :ivar rear: initial value: -1
    :ivar length: initial value: 0
    """
    def __init__(self, shape=(20, 2), dtype='float64'):
        """
        the queue has front pointer and the length.
        """
        from numpy import zeros, nan

        from threading import RLock, Lock
        self.lock = RLock()
        self.rear = 0  # the end of the Queue, where new date will be enquequ.
        self.global_rear = 0

        self.length = 0
        if 'float' in dtype:
            self.buffer = zeros(shape, dtype=dtype) * nan
        else:
            self.buffer = zeros(shape, dtype=dtype)

    def enqueue(self, data):
        """
        add (store) an item to the queue.

        Parameters
        ----------
        data :: (numpy array)
            data to append

        Returns
        -------

        Examples
        --------
        >>> queue = circular_buffer_numpy.queue.Queue(shape = (10,4)
        >>> from numpy.random import random
        >>> rand_arr = random(size=(6,4))
        >>> queue.enqueue(rand_arr)
        >>> queue.length
        6
        """
        from numpy import zeros
        if 'tuple' in str(type(data)) or 'lst' in str(type(data)):
            arr = zeros((len(data), 1))
            for idx in range(len(data)):
                arr[idx, 0] = data[idx]
        else:
            arr = data
        with self.lock:
            try:
                for j in range(arr.shape[0]):
                    self.buffer[self.rear] = arr[j]
                    self.rear += 1
                    self.global_rear += 1
                    if self.rear == self.shape[0]:
                        self.rear = 0

                    if self.length != self.shape[0]:
                        self.length += 1
            except Exception as err:
                error(err)


    def dequeue(self, N=0):
        """
        remove (access) an item from the queue.
        return N points from the back and move rear_pointer

        Parameters
        ----------
        N :: integer

        Returns
        -------
        array :: numpy array

        Examples
        --------
        >>> data = circual_buffer.Queue.dequeue()
        """
        with self.lock:
            rear = self.rear
            length = self.length
            shape = self.shape[0]
            debug(f'======== dequeue === start ======')
            debug(f'rear = {rear}')
            debug(f'length = {length}')
            debug(f'shape = {shape}')
            debug(f'N = {N}')
            if length >= N:
                i_pointer = rear - length
                if i_pointer < 0:
                    i_pointer =  shape + (i_pointer)
                j_pointer = rear - length + N
                if j_pointer < 0:
                    j_pointer = shape + (j_pointer)
                debug(f'i = {i_pointer}, f = {j_pointer}')
                data = self.peek_i_j(i_pointer, j_pointer)
                self.length -= N
            else:
                data = None
            debug(f'data shape = {data.shape}')
            debug(f'======== dequeue === end ======')
        return data

    # Few more functions are required to make the above-mentioned queue operation efficient. These are −
    @property
    def isfull(self):
        """
        Checks if the queue is full.

        Parameters
        ----------

        Returns
        -------
        flag :: boolean

        Examples
        --------
        >>> queue = Queue()
        >>> queue.isfull()
            False
        """
        return self.length >= self.shape[0]

    @property
    def isempty(self):
        """
        Checks if the queue is empty.

        Parameters
        ----------

        Returns
        -------
        flag :: boolean

        Examples
        --------
        >>> queue = Queue()
        >>> queue.isempty()
            True
        """
        return self.length == 0

    def reset(self):
        """
        resets the queue by setting front and back equal to 0.

        Parameters
        ----------

        Returns
        -------

        Examples
        --------
        >>> queue = Queue()
        >>> queue.reset()
        """
        self.rear = 0  # the last written element
        self.global_rear = 0
        self.length = 0  # the last read element

    def reshape(self, shape, dtype=None):
        """
        reshapes buffer but also resets it. Takes two parameters as input, shape and dtype.
        dtype atribute can be passed if dtype of the queue needs changes

        Parameters
        ----------
        shape :: tuple
            new shape of the queue
        dtype :: numpy datatype string
            new data type

        Returns
        -------

        Examples
        --------
        >>> queue = Queue(shape = (100,2))
        >>> queue.reshape(shape = (1000,2))
        >>> queue.shape
            (1000,2)
        """
        from numpy import zeros, nan
        if dtype is None:
            dtype = self.dtype
        if 'float' in dtype:
            self.buffer = zeros(shape, dtype=dtype) * nan
        else:
            self.buffer = zeros(shape, dtype=dtype)
        self.reset()

    @property
    def size(self):
        """
        integer: returns the size of the circular buffer
        """
        return self.buffer.size

    @property
    def shape(self):
        """
        tuple: returns the shape of the circular buffer
        """
        return self.buffer.shape

    @property
    def data_shape(self):
        """
        tuple: returns the shape of the circular buffer
        """
        return self.buffer.shape[1:]

    @property
    def get_dtype(self):
        """
        dtype: returns the dtype of the circular buffer
        """
        return self.buffer.dtype
    dtype = property(get_dtype)

# Extra functions that are used for peeking into the queue but not reading the data.
# Important for functioning of the queue

    def peek_i_j(self, i, j):
        """
        returns buffer between indices i and j (including index i)
        if j < i, it assumes that buffer wrapped around and will give information
        accordingly.
        NOTE: the user needs to pay attention to the order at which indices
        are passed
        NOTE: index i cannot be -1 otherwise it will return empty array
        """
        length = self.length
        if j > i:
            res = self.buffer[i:j]
        else:
            res = self.peek_N(N=length, M=j-1)
        return res

    def peek_N(self, N, M):
        """
        return N points before index M(including) in the circular buffer

        Parameters
        ----------
        N:  (integer)
            number of points requested before the pointer
        M:  (integer)
            pointer

        Returns
        -------
        array (numpy array)

        Examples
        --------
        >>> circual_buffer.Queue.peek_N()
        """
        from numpy import concatenate
        R = M
        if N-1 <= R:
            result = self.buffer[R-N:R]
        else:
            result = concatenate((self.buffer[-(N-R-1):], self.buffer[:R+1]), axis=0)

        return result

    def peek_last_N(self, N):
        """
        return last N entries

        Parameters
        ----------
        N:  (integer)
            number of points requested

        Returns
        -------
        array (numpy array)

        Examples
        --------
        >>> circual_buffer.Queue.peek_last_N()
        """
        from numpy import concatenate
        R = self.rear
        if N <= R:
            result = self.buffer[R-N:R]
        else:
            result = concatenate((self.buffer[R-N:], self.buffer[:R]), axis=0)
        return result

    def peek_all(self):
        """
        peeks into the queue and return entire buffer sorted. The last entry will be the end of the queue.
        """
        N = self.length
        return self.peek_last_N(N)

    def peek_rear(self):
        """
        Gets the element at the rear of the queue without removing it.
        """
        return self.buffer[self.rear]

    def peek_front(self):
        """
        Gets the element at the front of the queue without removing it.
        """
        return self.buffer[self.rear-self.length+1]


if __name__ == "__main__":  # for testing purposes
    from pdb import pm

    import traceback

    from time import time
    import logging
    from tempfile import gettempdir
    logging.basicConfig(filename=gettempdir()+'/circular_buffer.log',
                        level=logging.DEBUG, format="%(asctime)s %(levelname)s: %(message)s")

    queue = Queue()

    print("Circular buffer library")
    print("two classes: server and client")
    print("server = server() \nclient = client()")
    print("---------------------------")
    print("Server functions")
    print("server.append(data)")
    print("server.peek_all()")
    print("server.peek_N(N = integer)")
    print("---------------------------")
    print("Client functions")
    print("client.peek_all()")
    print("client.peek_update()")
    print("client.give_all()")
    print("client.give_N(N = integer)")
    print("---------------------------")
    print("Queue functions")
    print("arr = asarray([[1],[2]])")
    print("queue.enqueue(arr)")
    print("queue.dequeue(N = 1)")
    print("queue.isempty()")
    print("queue.isfull()")
    print("queue.front, queue.back")
    print("queue.size, queue.len, queue.type")
