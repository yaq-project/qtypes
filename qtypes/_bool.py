__all__ = ["Bool"]


from qtpy import QtCore, QtGui, QtWidgets

from ._base import Base
from ._signals import Signals


class Widget(Signals, QtWidgets.QCheckBox):
    pass


class Bool(Base):
    defaults = dict()
    defaults["value"] = False

    def _create_widget(self):
        return Widget()

    def on_updated(self, value):
        self._value.update(value)
        self._widget.setChecked(self._value["value"])
