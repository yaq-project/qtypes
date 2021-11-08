__all__ = ["Enum"]


from qtpy import QtCore, QtGui, QtWidgets

from ._base import Base
from ._signals import Signals


class Widget(Signals, QtWidgets.QComboBox):
    pass


class Enum(Base):
    defaults = dict()
    defaults["value"] = None
    defaults["allowed"] = []

    def _create_widget(self):
        return Widget()

    def on_updated(self, value):
        pass  # TODO:
