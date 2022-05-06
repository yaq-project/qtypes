__all__ = ["TreeWidget"]


import sys
import pathlib

from qtpy import QtWidgets, QtGui, QtCore

from ._base import Base
from ._styles import styles


__here__ = pathlib.Path(__file__).parent


class TreeWidget(QtWidgets.QTreeWidget):
    def __init__(self, model, *, include_root=True):
        width = 250
        super().__init__(parent=None, width=width)
        self.setColumnCount(2)
        self.setHeaderLabels(["", ""])
        sheets = list(styles["tomorrow-night"].values())
        self.setStyleSheet("".join(sheets))
        self.setColumnWidth(width // 2, width // 2)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.model = model
        self.include_root = include_root
        self._build_tree()

    def __getitem__(self, index):
        if index < 0:
            index = self.topLevelItemCount() + index
        return self.topLevelItem(index)

    def append(self, item):
        self.addTopLevelItem(item)
        if isinstance(item, Base):
            widget = item._widget
            widget.setParent(self)
            self.setItemWidget(item, 1, widget)
            self.children.append(item)

    def _build_tree(self):
        class Widget(QtWidgets.QWidget):
            def __init__(self, parent=None):
                super().__init__(parent=parent)
                # build widget
                self.setLayout(QtWidgets.QHBoxLayout())
                self.spin_box = QtWidgets.QDoubleSpinBox()
                self.layout().addWidget(self.spin_box)
                self.combo_box = QtWidgets.QComboBox()
                self.combo_box.setFixedWidth(100)
                self.combo_box.hide()  # will get shown if units are set
                self.layout().addWidget(self.combo_box)
                self.layout().setContentsMargins(0, 0, 0, 0)

        def make_widget(parent, model):
            wi = QtWidgets.QTreeWidgetItem([model.get()["label"], ""])
            parent.addChild(wi)
            widget = Widget(parent=self)
            self.setItemWidget(wi, 1, widget)
            for child in model.children:
                make_widget(wi, child)

        if not self.include_root:
            model = self.model.children
        else:
            model = self.model
        # top level items
        for m in model:
            wi = QtWidgets.QTreeWidgetItem([m.get()["label"], ""])
            self.addTopLevelItem(wi)
            widget = Widget(parent=self)
            self.setItemWidget(wi, 1, widget)
            for child in m.children:
                make_widget(wi, child)

    def clear(self):
        while self.children:
            child = self.children.pop(0)
            self.takeTopLevelItem(0)

    def insert(self, index, item):
        if index < 0:
            index += self.topLevelItemCount()
        if index < 0:
            index = 0
        if index > self.topLevelItemCount():
            index = self.topLevelItemCount()
        self.insertTopLevelItem(index, item)
        if isinstance(item, Base):
            widget = item._widget
            widget.setParent(self)
            self.setItemWidget(item, 1, widget)
            self.children.insert(index, item)
