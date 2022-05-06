__all__ = ["Base"]


from dataclasses import dataclass
from typing import Any, List

import qtpy
from qtpy import QtCore, QtGui, QtWidgets


class Base:
    def __init__(self, label="", value=None, disabled=False):
        self._data = dict()
        self._data["value"] = value
        self._data["disabled"] = disabled
        self._data["label"] = label
        self.children = []
        self._updated_callbacks = [self._on_updated]
        self._edited_callbacks = []

    def __getitem__(self, index):
        return self.children[index]

    def append(self, item):
        self.children.append(item)

    def clear(self):
        while self.children:
            self.children.pop(0)

    def insert(self, index, item):
        self.children.insert(index, item)

    def get(self) -> dict:
        return self._data

    def get_value(self) -> object:
        return self._value["value"]

    def _on_disabled(self, value: bool):
        self._widget.setDisabled(value)

    def _on_updated(self, value: dict):
        raise NotImplementedError

    def set(self, value: object):
        # TODO: diff check
        self._data.update(value)
        for cb in self._updated_callbacks:
            cb(self._data.as_dict())

    def set_value(self, value: object):
        if value != self._data.value:
            self._data.value = value
            for cb in self._updated_callbacks:
                cb(self._data.as_dict())

    @property
    def updated(self):
        return self._widget.updated
