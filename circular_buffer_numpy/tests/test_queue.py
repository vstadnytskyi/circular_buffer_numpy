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

    def test_queue_rear(self):
        """
        the freshly created queue has 'rear' value of 0 (the next available pointer in the queue buffer).
        """
        queue = Queue(shape=(100, 2, 2, 2))
        self.assertEqual(queue.rear, 0)

    def test_attributes(self):
        """
        various build-in attributes.
        """
        from numpy import random
        queue = Queue(shape=(100, 2, 3, 4), dtype='int16')
        data = random.randint(1024, size=(5, 2, 3, 4))
        self.assertEqual(queue.isempty, True)
        queue.enqueue(data)
        self.assertEqual(queue.length, 5)
        self.assertEqual(queue.rear, 5)
        self.assertEqual(queue.shape, (100, 2, 3, 4))
        self.assertEqual(queue.size, 100*2*3*4)
        self.assertEqual(queue.get_dtype, 'int16')
        self.assertEqual(queue.isfull, False)
        self.assertEqual(queue.isempty, False)

    def test_reshape(self):
        """
        reshaping operation
        """
        queue = Queue(shape=(100, 2, 3, 4), dtype='int16')
        queue.reshape(shape=(50, 2, 3, 4), dtype='float64')
        self.assertEqual(queue.length, 0)
        self.assertEqual(queue.rear, 0)
        self.assertEqual(queue.shape, (50, 2, 3, 4))
        self.assertEqual(queue.size, 50*2*3*4)
        self.assertEqual(queue.get_dtype, 'float64')

    def test_loop_around(self):
        queue = Queue(shape=(100, 2, 3, 4), dtype='int16')
        queue.reshape(shape=(50, 2, 3, 4), dtype='float64')
        self.assertEqual(queue.length, 0)
        self.assertEqual(queue.rear, 0)
        self.assertEqual(queue.shape, (50, 2, 3, 4))
        self.assertEqual(queue.size, 50*2*3*4)
        self.assertEqual(queue.get_dtype, 'float64')

    def test_peek_last_N(self):
        queue = Queue(shape=(10, 2, 3, 4), dtype='int16')
        self.assertEqual(queue.length, 0)
        self.assertEqual(queue.rear, 0)
        self.assertEqual(queue.shape, (10, 2, 3, 4))
        self.assertEqual(queue.size, 10*2*3*4)
        self.assertEqual(queue.get_dtype, 'int16')

        from numpy import random
        arr_rand = random.randint(4096,size = (25,2,3,4))
        queue.reset()
        j = 0
        for i in range(25):
            queue.enqueue(arr_rand[i].reshape(1,2,3,4))
            j+=1
            if j > queue.shape[0]:
                self.assertEqual(queue.length,queue.shape[0])
            else:
                self.assertEqual(queue.length,j)
            self.assertEqual((queue.peek_last_N(1) == arr_rand[i]).all(), True)

            #self.assertEqual(queue.rear,j)
            self.assertEqual(queue.global_rear,j)
        self.assertEqual((queue.peek_last_N(1) == arr_rand[-1]).all(), True)
        self.assertEqual((queue.peek_last_N(2) == arr_rand[-2:]).all(), True)
        self.assertEqual((queue.peek_last_N(5) == arr_rand[-5:]).all(), True)
        self.assertEqual((queue.peek_last_N(10) == arr_rand[-10:]).all(), True)

        dequeue_data = queue.dequeue(10)
        self.assertEqual(queue.length, 0)
        self.assertEqual(queue.rear, 5)
        self.assertEqual(queue.global_rear, 25)
        self.assertEqual((dequeue_data == arr_rand[-10:]).all(), True)

    def test_dequeue(self):
        """
        Testing dequeue operaritoin via writing and reading data from a queue multipletimes and keeping track of counters and length.
        """
        from numpy import random
        queue = Queue(shape=(11, 2, 3, 4), dtype='int16')
        for i in range(100):
            arr_in = random.randint(4096,size = (2,2,3,4))
            queue.enqueue(arr_in)
            arr_out = queue.dequeue(2)
            self.assertEqual((arr_in==arr_out).all(), True)
            self.assertEqual(queue.length,0)
            self.assertEqual(queue.global_rear,(i+1)*2)
            self.assertEqual(queue.rear,2*(i+1)-int(2*(i+1)/11)*11)

        from numpy import random
        queue = Queue(shape=(32, 2, 3, 4), dtype='int16')
        for i in range(100):
            arr_in = random.randint(4096,size = (1,2,3,4))
            queue.enqueue(arr_in)
            self.assertEqual(queue.length,1)
            arr_out = queue.dequeue(1)
            self.assertEqual((arr_in==arr_out).all(), True)
            self.assertEqual(queue.length,0)
            self.assertEqual(queue.global_rear,(i+1)*1)
            self.assertEqual(queue.rear,1*(i+1)-int(1*(i+1)/queue.shape[0])*queue.shape[0])


    def test_1(self):
        from numpy import std, random
        queue = Queue(shape=(100, 2, 2, 2))
        data = random.randint(0,1024, size=(5, 2, 2, 2))
        queue.enqueue(data)
        self.assertEqual(queue.length, 5)
        self.assertEqual(queue.rear, 5)
        queue.enqueue(data)
        dequeue_data = queue.dequeue(N=3)
        self.assertEqual(queue.length, 7)
        self.assertEqual(dequeue_data.shape, data[:3].shape)
        self.assertEqual(std(dequeue_data), std(data[:3]))

    def test_peek_N(self):
        queue = Queue(shape=(10, 2, 3), dtype='int16')
        self.assertEqual(queue.length, 0)
        self.assertEqual(queue.rear, 0)
        self.assertEqual(queue.shape, (10, 2, 3))
        self.assertEqual(queue.size, 10*2*3)
        self.assertEqual(queue.get_dtype, 'int16')

        from numpy import random
        arr_rand = random.randint(4096,size = (25,2,3))
        queue.reset()
        j = 0
        for i in range(25):
            queue.enqueue(arr_rand[i].reshape(1,2,3))
            j+=1
            if j > queue.shape[0]:
                self.assertEqual(queue.length,queue.shape[0])
            else:
                self.assertEqual(queue.length,j)
            self.assertEqual(queue.global_rear,j)
        self.assertEqual((queue.peek_N(1,0) == arr_rand[-1]).all(), True)

        self.assertEqual((queue.peek_N(2,1) == arr_rand[2]).all(), True)

        dequeue_data = queue.dequeue(10)
        self.assertEqual(queue.length, 0)
        self.assertEqual(queue.rear, 5)
        self.assertEqual(queue.global_rear, 25)
        self.assertEqual((dequeue_data == arr_rand[-10:]).all(), True)

    def test_1(self):
        from numpy import zeros
        from time import sleep
        queue = Queue(shape=(16, 2, 3), dtype='int16')
        for i in range(40):
            arr_in = zeros((1,2,3),dtype ='int16')+i
            queue.enqueue(arr_in)
            arr_out = queue.dequeue(1)
            self.assertEqual(i,arr_out[0,0,0])

        from ubcs_auxiliary.threading import new_thread

        def run(queue):
            for i in range(200):
                from time import sleep
                arr_in = zeros((1,2,3),dtype ='int16')+i
                queue.enqueue(arr_in)
                sleep(0.2)
        new_thread(run, queue)
        j = 0
        while j < 99:
            if queue.length > 0:
                arr_out = queue.dequeue(1)
                self.assertEqual(j,arr_out[0,0,0])
                j+=1
            sleep(0.03)
