#!/bin/env python
# -*- coding: utf-8 -*-
"""test Queue
    by Valentyn Stadnytskyi
     created: August 2, 2019
    This is a test library to evaluate the performance of the code.
    Queue is an abstract data structure, somewhat similar to Stacks.
    Unlike stacks, a queue is open at both its ends.
    One end is always used to insert data (enqueue)
    and the other is used to remove data (dequeue)

    to run unittest: python3 -m unittest test_queue
"""

import unittest

# from numpy.testing import assert_, assert_almost_equal, assert_equal

from ..queue import Queue


class QueueTest(unittest.TestCase):

    def test_queue_end(self):
        queue = Queue(shape=(100, 2))
        self.assertEqual(queue.rear, 0)

    def test_1(self):
        from numpy import std, random
        queue = Queue(shape=(100, 2))
        data = random.randint(1024, size=(5, 2))
        queue.enqueue(data)
        self.assertEqual(queue.length, 5)
        self.assertEqual(queue.rear, 5)
        queue.enqueue(data)
        dequeue_data = queue.dequeue(N=3)
        self.assertEqual(queue.length, 7)
        self.assertEqual(std(dequeue_data), std(data[:3]))

    def test_attributes(self):
        from numpy import random
        queue = Queue(shape=(100, 2), dtype='int16')
        data = random.randint(1024, size=(5, 2))
        self.assertEqual(queue.isempty, True)
        queue.enqueue(data)
        self.assertEqual(queue.length, 5)
        self.assertEqual(queue.rear, 5)
        self.assertEqual(queue.shape, (100, 2))
        self.assertEqual(queue.size, 100*2)
        self.assertEqual(queue.get_dtype, 'int16')
        self.assertEqual(queue.isfull, False)
        self.assertEqual(queue.isempty, False)

    def test_reshape(self):
        queue = Queue(shape=(100, 2), dtype='int16')
        queue.reshape(shape=(50, 2), dtype='float64')
        self.assertEqual(queue.length, 0)
        self.assertEqual(queue.rear, 0)
        self.assertEqual(queue.shape, (50, 2))
        self.assertEqual(queue.size, 50*2)
        self.assertEqual(queue.get_dtype, 'float64')
