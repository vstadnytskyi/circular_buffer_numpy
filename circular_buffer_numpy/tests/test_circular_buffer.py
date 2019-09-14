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

from ..circular_buffer import CircularBuffer


class QueueTest(unittest.TestCase):
    def test_queue_end(self):
        """
        test if the default pointer in the buffer is -1.
        """
        buffer = CircularBuffer(shape=(100, 2))
        self.assertEqual(buffer.pointer, -1)

    def test_queue_end_two(self):
        """
        test if the default pointer in the buffer is -1.
        """
        buffer = CircularBuffer(shape=(100, 2))
        self.assertEqual(buffer.pointer, -1)

    def test_1(self):
        from numpy import random
        buffer = CircularBuffer(shape=(100, 2))
        data = random.randint(1024, size=(5, 2))
        buffer.packet_length = 5
        buffer.append(data)
        self.assertEqual(buffer.pointer, 4)
        self.assertEqual(buffer.g_pointer, 4)
        self.assertEqual(buffer.packet_pointer, 0)
        self.assertEqual(buffer.g_packet_pointer, 0)

    def test_attributes(self):
        from numpy import random
        buffer = CircularBuffer(shape=(100, 2), dtype='int16')
        data = random.randint(1024, size=(5, 2))
        buffer.append(data)
        self.assertEqual(buffer.shape, (100, 2))
        self.assertEqual(buffer.size, 100*2)
        self.assertEqual(buffer.dtype, 'int16')
