__all__ = ["Base"]


from dataclasses import dataclass
from typing import Any, List

import qtpy
from qtpy import QtCore, QtGui, QtWidgets


class Base:
    qtype = "base"

    def __init__(self, label="", value=None, disabled=False):
        self._data = dict()
        self._data["value"] = value
        self._data["disabled"] = disabled
        self._data["label"] = label
        self.children = []
        self._updated_callbacks = []
        self._edited_callbacks = []
        self._restructured_callbacks = []

    def __getitem__(self, index):
        return self.children[index]

    def append(self, child):
        self.children.append(child)
        child.restructured_connect(self._restructured_emit)
        self._restructured_emit()

    def clear(self):
        while self.children:
            self.children.pop(0)
        self._restructured_emit()

    def edited_connect(self, function):
        self._edited_callbacks.append(function)

    def edited_disconnect(self, function):
        self._edited_callbacks.disconnect(function)

    def _edited_emit(self):
        for cb in self._edited_callbacks:
            cb(self._data)

    def insert(self, index, item):
        self.children.insert(index, item)

    def get(self) -> dict:
        return self._data

    def get_value(self) -> object:
        return self._data["value"]

    def restructured_connect(self, function):
        self._restructured_callbacks.append(function)

    def restructured_disconnect(self, function):
        self._restructured_callbacks.pop(function)

    def _restructured_emit(self):
        for cb in self._restructured_callbacks:
            cb()

    def set(self, value: object, *, from_widget=False):
        # TODO: diff check
        self._data.update(value)
        self._updated_emit()
        if from_widget:
            self._edited_emit()

    def set_value(self, value: object):
        self.set({"value": value})

    def updated_connect(self, function):
        self._updated_callbacks.append(function)

    def updated_disconnect(self, function):
        self._updated_callbacks.pop(function)

    def _updated_emit(self):
        for cb in self._updated_callbacks:
            cb(self._data)
