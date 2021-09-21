#!/bin/env python
# -*- coding: utf-8 -*-
"""test Queue
    by Valentyn Stadnytskyi
    created: August 2, 2019

    This is a test library to evaluate the performance of the code.
    Queue is an abstract data structure, somewhat similar to Stacks.
    Unlike stacks, a queue is open at both its ends.
    One end is always used to insert data (enqueue) and the other is used to remove data (dequeue)..

    to run unittest: python3 -m unittest test_queue
"""
import unittest
from numpy.testing import assert_array_equal

class CircularBufferTest(unittest.TestCase):
    def test_queue_end(self):
        """
        test if the default pointer in the buffer is -1.
        """
        from ..circular_buffer import CircularBuffer
        buffer = CircularBuffer(shape=(100, 2))
        self.assertEqual(buffer.pointer, -1)

    def test_queue_end_two(self):
        """
        test if the default pointer in the buffer is -1.
        """
        from ..circular_buffer import CircularBuffer
        buffer = CircularBuffer(shape=(100, 2))
        self.assertEqual(buffer.pointer, -1)

    def test_1(self):
        from numpy import random
        from ..circular_buffer import CircularBuffer
        buffer = CircularBuffer(shape=(100, 2, 4))
        data = random.randint(1024, size=(5, 2, 4))
        buffer.packet_length = 5
        buffer.append(data)
        self.assertEqual(buffer.pointer, 4)
        self.assertEqual(buffer.g_pointer, 4)
        self.assertEqual(buffer.packet_pointer, 0)
        self.assertEqual(buffer.g_packet_pointer, 0)

    def test_attributes(self):
        from ..circular_buffer import CircularBuffer
        from numpy import random
        buffer = CircularBuffer(shape=(100, 2), dtype='int16')
        data = random.randint(1024, size=(5, 2))
        buffer.append(data)
        self.assertEqual(buffer.shape, (100, 2))
        self.assertEqual(buffer.size, 100*2)
        self.assertEqual(buffer.dtype, 'int16')

    def test_full(self):
        from ..circular_buffer import CircularBuffer
        from numpy import random, sum
        buffer = CircularBuffer(shape=(100, 2, 3), dtype='float64')
        data = random.randint(1024, size=(50, 2, 3))
        buffer.append(data)
        assert buffer.pointer == 49
        assert buffer.g_pointer == 49
        assert buffer.shape == (100, 2, 3)
        assert buffer.size == buffer.buffer.shape[0]*buffer.buffer.shape[1]*buffer.buffer.shape[2]
        assert buffer.dtype == 'float64'
        assert sum(buffer.get_i_j(i=5, j=6)) == sum(buffer.buffer[5])
        # get data between pointers 5 and 10 and compare to get 5 points from pointer M
        assert sum(buffer.get_i_j(i=5, j=10)) == sum(buffer.get_N(N=5, M=9))

    def test_vector_append(self):
        from ..circular_buffer import CircularBuffer
        from numpy import random, sum, zeros, concatenate
        buffer = CircularBuffer(shape=(1000, 3))
        vec1 = zeros((1, 3))
        vec2 = zeros((1, 3))
        vec1[0, 0] = 0.0
        vec1[0, 1] = 1.0
        vec1[0, 2] = 2.0
        buffer.append(vec1)
        vec2[0, 0] = 3.0
        vec2[0, 1] = 4.0
        vec2[0, 2] = 5.0
        buffer.append(vec2)
        assert_array_equal(buffer.get_last_value(), vec2)
        assert_array_equal(buffer.get_last_N(2),concatenate((vec1, vec2)))


    def test_get_data(self):
        from ..circular_buffer import CircularBuffer
        from numpy import random, sum, zeros, concatenate, array
        buffer = CircularBuffer(shape=(1000, 3))
        res_buffer = []

        j = 0
        for i in range(5):
            vec = zeros((3,))
            vec[0] = j
            vec[1] = j**2
            vec[2] = j**3
            buffer.append(vec)
            res_buffer.append(vec)
            j+=1
        assert_array_equal(array(res_buffer),buffer.get_data())

        for i in range(555):
            vec = zeros((3,))
            vec[0] = j
            vec[1] = j**2
            vec[2] = j**3
            buffer.append(vec)
            res_buffer.append(vec)
            j+=1
        assert_array_equal(array(res_buffer),buffer.get_data())

        #the 1000-long buffer spils over and overwrites existing values. The function get_data returns only
        for i in range(1300):
            vec = zeros((3,))
            vec[0] = j
            vec[1] = j**2
            vec[2] = j**3
            buffer.append(vec)
            res_buffer.append(vec)
            j+=1
        assert_array_equal(array(res_buffer[-1000:]),buffer.get_data())

    def test_get_N(self):
        from ..circular_buffer import CircularBuffer
        from numpy import random, sum, zeros, concatenate, array
        buffer = CircularBuffer(shape=(102, 2))
        for pointer in range(1000):
            while pointer >= (buffer.shape[0]):
                pointer = int(pointer - buffer.shape[0])
            data = buffer.get_N(3,pointer)
            self.assertEqual(data.shape, (3,2))

    def test_different_dtype(self):
        from ..circular_buffer import CircularBuffer
        import numpy

        buffer_int16 = CircularBuffer(shape=(102, 2), dtype = numpy.int16)
        buffer_int32 = CircularBuffer(shape=(102, 2), dtype = numpy.int32)
        buffer_int64 = CircularBuffer(shape=(102, 2), dtype = numpy.int64)
        buffer_float32 = CircularBuffer(shape=(102, 2), dtype = numpy.float32)
        buffer_float64 = CircularBuffer(shape=(102, 2), dtype = numpy.float64)

        self.assertEqual(buffer_int16.dtype, numpy.int16)
        self.assertEqual(buffer_int16.dtype, numpy.int16)
        self.assertEqual(buffer_int32.dtype, numpy.int32)
        self.assertEqual(buffer_int64.dtype, numpy.int64)
        self.assertEqual(buffer_float32.dtype, numpy.float32)
        self.assertEqual(buffer_float64.dtype, numpy.float64)
