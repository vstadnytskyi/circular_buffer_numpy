#!/bin/env python
# -*- coding: utf-8 -*-
"""Circular buffer Server and Client module
    by Valentyn Stadnytskyi
    created: Nov 4, 2017
    last update: February, 2019

    contains 2 classes: Server and Client circular buffer. Are very similar except

    1.0.4 - var_type = 'float32' was replaced with 'float64' as a default data type in the server buffer.
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
__version__  = '1.1.8'

from logging import debug, info,warn,error
from numpy import nan, zeros, ones, asarray, transpose, concatenate
import warnings
from pdb import pm
import traceback

################################################################################################################
#### Client section of the Circular Buffer
################################################################################################################
class CircularBufferClient(object):
    """
    circular buffer client (cbclient). has its' own buffer,
    keeps track of last known server pointer(self.pointerS)
    and current client pointer(self.pointerC)

    functions:
    get_all: FIXIT
    get_updata: FIXIT
    give_all: returns entire circular buffer client
    give_N: FIXIT
    """
    def __init__(self, size=(4, 1000), var_type='float64'): #Client buffer does not need type since it is always updated with the server buffer.
        self.size = size
        #if type(self.size) is not tuple:
            #raise ValueError('Client circular buffer: the circular buffer size should be tuple but', type(self.size), 'is found')
        self.var_type = var_type
        self.type = 'client'
        self.buffer = zeros(self.size,dtype=var_type) * nan # tuple (smaller, large) dimensions
        self.__info__ = "Client RingBuffer"
        self.pointerC = -1 #Client pointer
        self.pointerS = -1 #Server pointer

    def append(self,data):
        """
        append function for client circular buffer. Appends data to an existing circular buffer
        """
        from numpy import zeros
        if 'tuple' in str(type(data)) or 'lst' in str(type(data)):
            arr = zeros((len(data),1))
            for idx in range(len(data)):
                arr[idx,0] = data[idx]
        else:
            arr = data
        try:
            len_j = arr.shape[1]
            flag = True
        except:
            len_j = 1
            flag = False
        if flag:
            for j in range(len_j):
                if self.pointerC == self.size[1]-1:
                    self.pointerC = -1
                for i in range(self.size[0]):
                    self.buffer[i,self.pointerC+1] = arr[i,j]
                self.pointerC = self.pointerC + 1
        else:
            if self.pointerC == self.size[1]-1:
                self.pointerC = -1
            for i in range(self.size[0]):
                self.buffer[i,self.pointerC+1] = arr[i]
            self.pointerC = self.pointerC + 1



    def get_all(self,pointerS,input_data):
        """
        the name get is misleading here. This is set_all.
        It sets server(self.pointerS) and client(self.pointerC)
        to the pointerS input value and makes the self.buffer = input_data
        """
        self.buffer = input_data
        self.pointerS = pointerS
        self.pointerC = pointerS

    def update(self,pointerS,input_data): # takes server pointer and calculates how many to
        """
        pointerS - CBServer pointer
        input_data - input data

        """
        if type(pointerS) != int:
            raise ValueError('Client circular buffer: the server pointer has to be integer, instead got', type(pointerS))
        for j in range(len(input_data[0,:])):
            if self.pointerC == len(self.buffer[0,:]): #if client pointer becomes length of the buffer, assign it to zero (wrap arround)
                self.pointerC = 0
            self.buffer[:,self.pointerC] = input_data[:,j]
            self.pointerC = self.pointerC + 1
            self.pointerS = self.pointerS + 1

    def give_all(self):
        """
        returns entire self.buffer
        """
        response = self.give_N(N = self.size[1])
        return self.buffer

    def give_N(self, N):
        """
        returns last N entries before the known client pointer(self.pointerC)
        Valentyn: June 15 FIXIT I am not sure what this function is supposed to do
        """
        P = self.pointerC
        if N-1 <= P:
            result = self.buffer[:,P+1-N:P+1]
        else:
            result = concatenate((self.buffer[:,-(N-P-1):], self.buffer[:,:P+1]),axis = 1)
        return result

    def clear(self):
        """
        clears the buffer.
        if type is float will make it all nan
        if type is not float will make it just 0
        resets both pointers to -1.

        Parameters
        ----------
        Returns
        -------

        Examples
        --------
        >>> circual_buffer.clear()

        """
        if 'float' in self.var_type:
            self.buffer = self.buffer * nan
        else:
            self.buffer = self.buffer*0
        self.pointerC = -1
        self.pointerS = -1



CircularBufferClient.reset = CircularBufferClient.clear

CBClient = CircularBufferClient

if __name__ == "__main__": # for testing purposes
    from time import time
    import logging
    from tempfile import gettempdir
    logging.basicConfig(#filename=gettempdir()+'/circular_buffer_LL.log',
                        level=logging.DEBUG, format="%(asctime)s %(levelname)s: %(message)s")


    server = Server()
    client = Client()
    queue = Queue()

    print("Circular buffer library")
    print("two classes: server and client")
    print("server = server() \nclient = client()")
    print("---------------------------")
    print("Server functions")
    print("server.append(data)")
    print("server.get_all()")
    print("server.get_N(N = integer)")
    print("---------------------------")
    print("Client functions")
    print("client.get_all()")
    print("client.get_update()")
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
