#!/bin/env python
# -*- coding: utf-8 -*-
"""Circular buffer Server
    by Valentyn Stadnytskyi
    created: Nov 4, 2017
    last update: February, 2019
"""
import logging
from logging import debug, info, warn, error
import warnings
logging.getLogger(__name__).addHandler(logging.NullHandler())

class CircularBuffer(object):
    """
    :ivar pointer: initial value: -1
    :ivar g_pointer: initial value: -1
    :ivar packet_length: initial value 1
    """
    pointer = -1 # running current pointer value
    g_pointer = -1 # running current global_pointer value

    def __init__(self, shape=(100, 2), dtype='float64', packet_length=1):
        from numpy import nan, zeros, empty
        """
        initializes the class. creates an empty numpy array with given size and give dtype.
        the shape follows numpy definition where the first index corresponds to x or col and second is y or row.
        populates the array with nan if dtype is float or zeros if else.
        creates attributes:
        __info__,
        name,
        size,
        dtype,
        type,
        packet_length,
        pointer
        g_pointer
        packet_pointer
        g_packet_pointer
        """
        self.__info__ = "Server RingBuffer"
        self.name = 'circular buffer server'
        self.type = 'server'
        self.packet_length = packet_length

        self.buffer = empty(shape, dtype=dtype)

    def append(self, data):
        """
        appends data to the existing circular buffer.

        Parameters
        ----------
        data :: (numpy array)
            data to append

        Returns
        -------

        Examples
        --------
        >>> buffer = circular_buffer_numpy.circular_buffer.CircularBuffer(shape = (10,4)
        >>> from numpy.random import random
        >>> rand_arr = random(size=(6,4))
        >>> buffer.append(rand_arr)
        >>> buffer.pointer
        5
        """
        if len(data.shape) == len(self.shape)-1:
            data = data.reshape((1,data.shape[0]))
        for i in range(data.shape[0]):
            if self.pointer == self.shape[0]-1:
                self.pointer = -1
            self.buffer[self.pointer+1] = data[i]
            self.pointer += 1
            self.g_pointer += 1

    def reset(self, clear=False):
        """
        resets pointers to -1 (empty buffer), the full reset can be force via parameter clears
        The parameter clear can be used to

        Parameters
        ----------
        clear ::  (boolean)
            force clearing the buffer

        Returns
        -------

        Examples
        --------
        >>> circual_buffer.CircularBuffer.reset()
        """
        from numpy import nan
        if clear:
            if 'float' in self.type:
                self.buffer = self.buffer * nan
            else:
                self.buffer = self.buffer*0
        self.pointer = -1
        self.g_pointer = -1
        debug('{},{}'.format(self.pointer, self.g_pointer))

    def change_length(self, length):
        """
        changes length of the buffer

        Parameters
        ----------
        length ::  integer
            new length of the buffer

        Returns
        -------

        Examples
        --------
        >>> buffer = circual_buffer.CircularBuffer(shape=(10,4))
        >>> buffer.shape
        (10,4)
        >>> buffer.change_length(12)
        >>> buffer.shape
        (12,4)
        """
        from numpy import zeros, nan, copy
        old_buffer = self.get_all()
        new_length = [length] + list(data_shape)
        self.buffer = zeros(shape=new_length, dtype=self.dtype) * nan
        self.append(old_buffer)

    def get_all(self):
        """
        return entire circular buffer server in ordered way, where
        last value is the last collected.

        Parameters
        ----------

        Returns
        -------
        array (numpy array)

        Examples
        --------
        >>> data = circual_buffer.CircularBuffer.get_all()
        """
        return self.get_last_N(N=self.shape[0])

    def get_data(self):
        """
        return all valid circular buffer entries in ordered way, where
        last value is the last collected.

        Parameters
        ----------

        Returns
        -------
        array (numpy array)

        Examples
        --------
        >>> data = circual_buffer.CircularBuffer.get_data()
        """
        if self.g_pointer + 1 < self.length:
            return self.get_last_N(self.g_pointer+1)
        else:
            return self.get_all()

    def get_last_N(self, N):
        """
        returns last N entries from the known self.pointer(circular buffer pointer)

        Parameters
        ----------
        N :: (integer)
            number of points to return

        Returns
        -------
        array (numpy array)

        Examples
        --------
        >>> data = circual_buffer.CircularBuffer.get_last_N(10)
        """
        from numpy import concatenate
        P = self.pointer
        if N-1 <= P:
            result = self.buffer[P+1-N:P+1]
        else:
            result = concatenate((self.buffer[-(N-P-1):], self.buffer[:P+1]), axis=0)
        return result

    def get_last_value(self):
        """
        returns last entry from the known. Same as self.buffer[self.pointer]

        Parameters
        ----------

        Returns
        -------
        array (numpy array)

        Examples
        --------
        >>> data = circual_buffer.CircularBuffer.get_last_value()
        """
        return self.get_last_N(N=1)

    def get_value(self, linear_pointer = None, circular_pointer = None):
        """
        returns last entry from the known. Same as self.buffer[self.pointer]

        Parameters
        ----------

        Returns
        -------
        array (numpy array)

        Examples
        --------
        >>> data = circual_buffer.CircularBuffer.get_last_value()
        """
        if (linear_pointer is  None) and (circular_pointer is None):
            raise Exception('linear_pointer or circular_pointer has to be supplied. None were supplied.')
        if (linear_pointer is not  None) and (circular_pointer is not None):
            raise Exception('linear_pointer or circular_pointer has to be supplied, not both.')
        if (linear_pointer is not None) and (circular_pointer is None):
            pointer = linear_pointer - self.length*(linear_pointer//self.length)
        if (linear_pointer is  None) and (circular_pointer is not None):
            if not circular_pointer>self.length:
                pointer = circular_pointer
            else:
                raise Exception('circular_pointer exceeds the length of the buffer')
        return self.buffer[pointer]

    def get_i_j(self, i, j):
        """
        returns buffer between indices i and j (including index i)
        if j < i, it assumes that buffer wrapped around and will give information
        accordingly.
        NOTE: the user needs to pay attention to the order at which indices
        are passed
        NOTE: index i cannot be -1 otherwise it will return empty array

        Parameters
        ----------
        i :: (integer)
            start index in the buffer
        j :: (integer)
            end index in the buffer

        Returns
        -------
        array (numpy array)

        Examples
        --------
        >>> data = circual_buffer.CircularBuffer.get_i_j(i=2,j=5)
        """
        if j > i:
            res = self.buffer[i:j]
        else:
            length = self.shape[0] - i + j
            res = self.get_N(N=length, M=j-1)
        return res

    def get_N(self, N=0, M=0):
        """
        return N points before index M in the circular buffer

        Parameters
        ----------
        N :: (integer)
            number of points to return
        M :: (integer)
            index of the pointer

        Returns
        -------
        array (numpy array)

        Examples
        --------
        >>> data = circual_buffer.CircularBuffer.get_N(N=2, M=5)
        """
        from numpy import concatenate
        P = M
        if N-1 <= P:
            result = self.buffer[P+1-N:P+1]
        else:
            result = concatenate((self.buffer[-(N-P-1):], self.buffer[:P+1]), axis=0)
        return result

    def get_N_global(self, N=0, M=0):
        """
        return N points before global index M in the circular buffer.

        Parameters
        ----------
        N :: (integer)
            number of points to return
        M :: (integer)
            global index of the pointer

        Returns
        -------
        array (numpy array)

        Examples
        --------
        >>> data = circual_buffer.CircularBuffer.get_N(N=2, M=5)
        """
        from numpy import concatenate
        P = M

        while M >= self.shape[0]:
            M = M - self.shape[0]
        P = M

        if N-1 <= P:
            result = self.buffer[P+1-N:P+1]
        else:
            result = concatenate((self.buffer[-(N-P-1):], self.buffer[:P+1]), axis=0)
        return result

    @property
    def g_packet_pointer(self):
        """
        returns global packet pointer calculated from global pointer and packet size.
        The packet pointer can be a float number. It serves as an indaction something was not appended in packets.
        """
        return ((self.g_pointer+1)/self.packet_length)-1

    @property
    def packet_pointer(self):
        """
        returns packet pointer calculated from local pointer and packet size.
        The packet pointer can be a float number. It serves as an indaction something was not appended in packets.
        """
        return ((self.pointer+1)/self.packet_length)-1

    @property
    def size(self):
        """
        integer: property objects that returns the size of the circular buffer.
        """
        debug('returing size')
        return self.buffer.size

    @property
    def shape(self):
        """
        tuple: property objects that returns the shape of the circular buffer.
        """
        return self.buffer.shape

    def get_length(self):
        """
        integer: returns the length of the circular buffer along fast
        """
        return self.buffer.shape[0]
    length = property(get_length)

    @property
    def data_shape(self):
        """
        tuple: property objects that returns the shape of one data point
        (or N dimensional array) of the circular buffer
        """
        return self.buffer.shape[1:]

    @property
    def dtype(self):
        """
        dtype: property objects that returns the shape of one data point
        (or N dimensional array) of the circular buffer
        """
        return self.buffer.dtype

    @property
    def linear_pointer(self):
        """
        'linear pointer' refers to a global pointer that has been counting from the beginning of times.
        """
        return self.g_pointer
    @property
    def circular_pointer(self):
        """
        'circular pointer' refers to an actual pointer in the circular buffer numpy array and is an alias of 'pointer'
        """
        return self.pointer


if __name__ == "__main__":  # for testing purposes
    from pdb import pm  # for debugging
    from time import time
    import logging
    from tempfile import gettempdir
    import traceback

    #https://docs.python.org/3/library/logging.html#logrecord-attributes
    from tempfile import gettempdir
    logging.basicConfig(filename=gettempdir()+'/circular_buffer_LL.log',
                level=logging.DEBUG,
                format="%(asctime)-15s|PID:%(process)-6s|%(levelname)-8s|%(name)s| module:%(module)s-%(funcName)s|message:%(message)s")

    print("Circular buffer library")
    print("two classes: server and client")
    print("server = server() \nclient = client()")
    print("---------------------------")
    print("Server functions")
    print("server.append(data)")
    print("server.get_all()")
    print("server.get_N(N = integer)")
    print("---------------------------")
