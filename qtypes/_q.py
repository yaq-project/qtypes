"""Core enqueue and dequeue code."""


import time

import qtpy
from qtpy import QtCore, QtGui, QtWidgets


class Enqueued(QtCore.QMutex):
    def __init__(self):
        """
        Holds list of enqueued options.
        """
        QtCore.QMutex.__init__(self)
        self.value = []

    def read(self):
        return self.value

    def push(self, value):
        self.lock()
        self.value.append(value)
        self.unlock()

    def pop(self):
        self.lock()
        self.value = self.value[1:]
        self.unlock()


class Q:
    def __init__(self, enqueued, busy, driver):
        self.enqueued = enqueued
        self.busy = busy
        self.driver = driver
        self.queue = QtCore.QMetaObject()

    def push(self, method, *args, **kwargs):
        print("Q PUSH", method, args, kwargs)
        self.enqueued.push([method, time.time()])
        self.busy.write(True)
        # send Qt SIGNAL to address thread
        self.queue.invokeMethod(
            self.driver,
            "dequeue",
            QtCore.Qt.QueuedConnection,
            QtCore.Q_ARG(str, method),
            QtCore.Q_ARG(list, [args, kwargs]),
        )
