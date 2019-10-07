#!/bin/env python
# -*- coding: utf-8 -*-
from circular_buffer_numpy import __version__
from circular_buffer_numpy.circular_buffer import CircularBuffer
print('circular buffer number version: {}'.format(__version__))
import timeit
data_dim = 1000
buffer = CircularBuffer(shape=(1000000, data_dim))
from numpy import random
data = random.randint(2**16, size=(1000, data_dim))

def write():
    buffer.append(data)

def read_N(N = 1000):
    data = buffer.get_last_N(N)

header = ['N','data_dim','number','time']
number_lst = [1000000,100000,10000,1000,100]
N_lst = [1,10,100,1000,10000]
data_dim_lst = [10,100,1000]
t_lst = []
for data_dim in data_dim_lst:
    buffer = CircularBuffer(shape=(1000000, data_dim))
    for N in N_lst:
        number = number_lst[N_lst.index(N)]
        data = random.randint(2**16, size=(N, data_dim))
        t = timeit.timeit(write, number=number)
        t_lst.append([N,data_dim,number,t/number])
        print('{} per write of {}x{} array'.format(t/number,N,data_dim))

del buffer
def plot():
    from matplotlib import pyplot as plt
    fig = plt.figure()
    from numpy import asarray, where
    t_arr = asarray(t_lst)
    plt.loglog(t_arr[where(t_arr[:,1] == 10),0],t_arr[where(t_arr[:,1] == 10),3],'-or', label = 'width = 10')
    plt.loglog(t_arr[where(t_arr[:,1] == 100),0],t_arr[where(t_arr[:,1] == 100),3],'-og', label = 'width = 100')
    plt.loglog(t_arr[where(t_arr[:,1] == 1000),0],t_arr[where(t_arr[:,1] == 1000),3],'-ob', label = 'width = 1000')
    plt.xlabel('N, circular dimension length')
    plt.ylabel('time to write')
    plt.title('Time to write vs data dimensions (length x width)')
    f.savefig("benchmarks-{}.pdf".format(__version__), bbox_inches='tight')
plot()
