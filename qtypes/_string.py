__all__ = ["String"]


from qtpy import QtCore, QtGui, QtWidgets

from ._base import Base
from ._signals import Signals


class Widget(Signals, QtWidgets.QLineEdit):
    pass


class String(Base):
    defaults = dict()
    defaults["value"] = ""

    def _create_widget(self):
        return Widget()

    def on_updated(self, value):
        self._value.update(value)
        self._widget.setText(self._value["value"])
