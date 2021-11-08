__all__ = ["Integer"]


from qtpy import QtWidgets, QtGui

from ._base import Base
from ._signals import Signals


class Widget(Signals, QtWidgets.QSpinBox):
    pass


class Integer(Base):
    defaults = dict()
    defaults["value"] = float("nan")
    defaults["minimum"] = float("-inf")
    defaults["maximum"] = float("inf")

    def _create_widget(self):
        return Widget()

    def on_updated(self, value):
        pass  # TODO:
