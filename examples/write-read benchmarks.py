from circular_buffer_numpy import __version__
from circular_buffer_numpy.circular_buffer import CircularBuffer

from numpy import random, asarray, where, savetxt
from matplotlib import pyplot as plt
import timeit

print('circular buffer numpy version: {}'.format(__version__))
data_dim = 1000
buffer = CircularBuffer(shape=(1000000, data_dim))
data = random.randint(2**16, size=(1000, data_dim))


def write():
    global buffer
    buffer.append(data)


def read():
    global buffer
    data = buffer.get_last_N(N)
    return data


header = ['N', 'data_dim', 'number', 'write time', 'read time']
number_lst = [1000000, 100000, 10000, 1000, 100]
N_lst = [1, 10, 100, 1000, 10000]
data_dim_lst = [10, 100, 1000]
t_lst = []
for data_dim in data_dim_lst:
    buffer = CircularBuffer(shape=(1000000, data_dim))
    for N in N_lst:
        number = number_lst[N_lst.index(N)]
        data = random.randint(2**16, size=(N, data_dim))
        t_write = timeit.timeit(write, number=number)
        t_read = timeit.timeit(read, number=number)
        t_lst.append([N, data_dim, number, t_write/number, t_read/number])
        print('{} per write and {} per read of {}x{} array'.format(t_write/number, t_read/number, N, data_dim))
    del buffer

t_arr = asarray(t_lst)
fig = plt.figure()


plt.loglog(t_arr[where(t_arr[:, 1] == 10), 0], t_arr[where(t_arr[:, 1] == 10), 3], '-or')
plt.loglog(t_arr[where(t_arr[:, 1] == 100), 0], t_arr[where(t_arr[:, 1] == 100), 3], '-og')
plt.loglog(t_arr[where(t_arr[:, 1] == 1000), 0], t_arr[where(t_arr[:, 1] == 1000), 3], '-ob')
plt.xlabel('N, circular dimension length')
plt.ylabel('time to write, seconds')
title = 'Time to write vs data dimensions (length x width) \n'
title += 'where width equal to red: 10; green: 100; blue: 1000'
plt.title(title)
fig.savefig("write-benchmarks-{}.jpg".format(__version__), bbox_inches='tight')

fig = plt.figure()
from matplotlib import pyplot as plt
plt.loglog(t_arr[where(t_arr[:, 1] == 10), 0], t_arr[where(t_arr[:, 1] == 10), 4], '-or')
plt.loglog(t_arr[where(t_arr[:, 1] == 100), 0], t_arr[where(t_arr[:, 1] == 100), 4], '-og')
plt.loglog(t_arr[where(t_arr[:, 1] == 1000), 0], t_arr[where(t_arr[:, 1] == 1000), 4], '-ob')
plt.xlabel('N, circular dimension length')
plt.ylabel('time to read, seconds')
title = 'Time to write vs data dimensions (length x width) \n'
title += 'where width equal to red: 10; green: 100; blue: 1000'
plt.title(title)
fig.savefig("read-benchmarks-{}.jpg".format(__version__), bbox_inches='tight')


savetxt("write-read-benchmarks-{}.txt".format(__version__), t_arr)
