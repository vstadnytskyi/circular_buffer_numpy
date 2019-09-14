#!/bin/env python
# -*- coding: utf-8 -*-
"""Circular buffer Server
    by Valentyn Stadnytskyi
    created: Nov 4, 2017
    last update: February, 2019

    contains 2 classes: Server and Client circular buffer. Are very similar except

    1.0.4 - dtype = 'float32' was replaced with 'float64' as a default data type in the server buffer.
            This solves problem is one is trying to use epoch time.
    1.1.0   - cathing exception in server append function in case
                the input data has wrong format
            - added logging
    1.1.1   - buffer start as nan instead of 0 or 1
                this actually caused a lot of problem with standard numpy functions
                that do not work with nan. However, there is often a version that
                works with nan(e.g. max -> nanmax)
    1.1.2   - nan cannot be encoded in int array. if array is multiplied by nan
                its' type gets converted to float
            - fixed appending of a tuple with size (2,)
            - added names CBserver(Circular Buffer server)
                and CBclient(Circrula Buffer client)
                the server and client are kept for back compatibility

    1.1.3   - Added append function to the client circular buffer

    1.1.4   - Added clear function to both client and server, that will clear the buffers and reset counters.

    1.1.5 - fixed python 3 competability

"""

__version__ = '1.1.8'

from logging import debug, info, warn, error
import warnings
# Client section of the Circular Buffer


class CircularBuffer(object):
    """
    Description for class

    :ivar pointer: initial value: -1
    :ivar g_pointer: initial value: -1
    :ivar packet_length: initial value 1
    """
    def __init__(self, shape=(100, 2), dtype='float64', packet_length=1):
        from numpy import nan, zeros
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
        self.pointer = -1
        """ running current pointer value """
        self.g_pointer = -1
        """ running current global_pointer value """
        self.lenngth = shape[0]
        self.datapoint_shape = shape[1:]
        if 'float' in dtype:
            self.buffer = zeros(shape, dtype=dtype) * nan
        else:
            self.buffer = zeros(shape, dtype=dtype)

    def append(self, data):
        """
        appends data to the existing circular buffer.
        """
        from numpy import zeros
        if 'tuple' in str(type(data)):
            arr = zeros((len(data), 1))
            for idx in range(len(data)):
                arr[idx, 0] = data[idx]
        else:
            arr = data
        try:
            if arr is not None:
                for i in range(arr.shape[0]):
                    if self.pointer == self.shape[0]-1:
                        self.pointer = -1
                    self.buffer[self.pointer+1] = arr[i]
                    self.pointer += 1
                    self.g_pointer += 1
        except Exception:
            error(traceback.format_exc())

    def reset(self, clear=False):
        """
        resets pointers to -1 (empty buffer), the full reset can be force via parameter clears
        The parameter clear can be used to

        Parameters
        ----------
        clear:  (boolean)
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

    def reshape(self, shape, dtype=None):
        from numpy import zeros, nan
        if dtype is None:
            dtype = self.dtype
        if 'float' in self.dtype:
            self.buffer = zeros(shape, dtype=self.dtype) * nan
        else:
            self.buffer = zeros(shape, dtype=self.dtype)

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

    def get_last_N(self, N):
        """
        returns last N entries from the known self.pointer(circular buffer pointer)
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
        returns last entry in the circular buffer
        """
        return self.get_last_N(N=1)

    def get_i_j(self, i, j):
        """
        returns buffer between indices i and j (including index i)
        if j < i, it assumes that buffer wrapped around and will give information
        accordingly.
        NOTE: the user needs to pay attention to the order at which indices
        are passed
        NOTE: index i cannot be -1 otherwise it will return empty array
        """
        if j > i:
            res = self.buffer[i:j]
        else:
            length = self.shape[1] - i + j
            res = self.get_N(N=length, M=j-1)
        return res

    def get_N(self, N=0, M=0):
        """
        return N points before index M in the circular buffer
        """
        from numpy import concatenate
        P = M
        if N-1 <= P:
            result = self.buffer[P+1-N:P+1]
        else:
            result = concatenate((self.buffer[-(N-P-1):], self.buffer[:P+1]), axis=1)
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


if __name__ == "__main__":  # for testing purposes
    from pdb import pm  # for debugging
    from time import time
    import logging
    from tempfile import gettempdir
    import traceback

    logging.basicConfig(filename=gettempdir()+'/circular_buffer_LL.log',
                        level=logging.DEBUG, format="%(asctime)s %(levelname)s: %(message)s")

    print("Circular buffer library")
    print("two classes: server and client")
    print("server = server() \nclient = client()")
    print("---------------------------")
    print("Server functions")
    print("server.append(data)")
    print("server.get_all()")
    print("server.get_N(N = integer)")
    print("---------------------------")
