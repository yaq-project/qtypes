__all__ = ["Button"]


from qtpy import QtWidgets, QtGui

from ._base import Base
from ._signals import Signals


class Widget(Signals, QtWidgets.QPushButton):
    pass


class Button(Base):
    defaults = dict()

    def _create_widget(self):
        self._widget = Widget("button")
        self._widget.clicked.connect(self._on_clicked)
        return self._widget

    def _on_clicked(self):
        self.updated.emit({})

    def on_updated(self, value):
        pass  # TODO:
