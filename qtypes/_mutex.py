"""Core mutex code."""


import os
import time

import numpy as np

import qtpy
from qtpy import QtCore, QtGui, QtWidgets


class Mutex(QtCore.QMutex):
    def __init__(self, initial_value=None):
        QtCore.QMutex.__init__(self)
        self.WaitCondition = QtCore.QWaitCondition()
        self.value = initial_value

    def read(self):
        return self.value

    def write(self, value):
        self.lock()
        self.value = value
        self.WaitCondition.wakeAll()
        self.unlock()

    def wait_for_update(self, timeout=5000):
        if self.value:
            return self.WaitCondition.wait(self, msecs=timeout)


class Busy(QtCore.QMutex):
    def __init__(self):
        """
        QMutex object to communicate between threads that need to wait \n
        while busy.read(): busy.wait_for_update()
        """
        QtCore.QMutex.__init__(self)
        self.WaitCondition = QtCore.QWaitCondition()
        self.value = False
        self.type = "busy"
        self.update_signal = None

    def read(self):
        return self.value

    def write(self, value):
        """
        bool value
        """
        self.tryLock(10)  # wait at most 10 ms before moving forward
        self.value = value
        self.unlock()
        self.WaitCondition.wakeAll()

    def wait_for_update(self, timeout=5000):
        """
        wait in calling thread for any thread to call 'write' method \n
        int timeout in milliseconds
        """
        if self.value:
            return self.WaitCondition.wait(self, msecs=timeout)


class Data(QtCore.QMutex):
    def __init__(self):
        QtCore.QMutex.__init__(self)
        self.WaitCondition = QtCore.QWaitCondition()
        self.shape = (1,)
        self.size = 1
        self.channels = []
        self.cols = []
        self.signed = []
        self.map = None

    def read(self):
        return self.channels

    def read_properties(self):
        """
        Returns
        -------
        tuple
            shape, cols, map
        """
        self.lock()
        outs = self.shape, self.cols, self.map
        self.unlock()
        return outs

    def write(self, channels):
        self.lock()
        self.channels = channels
        self.WaitCondition.wakeAll()
        self.unlock()

    def write_properties(self, shape, cols, channels, signed=False, map=None):
        self.lock()
        self.shape = shape
        self.size = np.prod(shape)
        self.channels = channels
        self.cols = cols
        self.signed = signed
        if not signed:
            self.signed = [False] * len(self.cols)
        self.map = map
        self.WaitCondition.wakeAll()
        self.unlock()

    def wait_for_update(self, timeout=5000):
        if self.value:
            return self.WaitCondition.wait(self, msecs=timeout)
