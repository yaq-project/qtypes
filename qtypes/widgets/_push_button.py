__all__ = ["PushButton"]


import collections
import os


from PySide2 import QtWidgets


class PushButton(QtWidgets.QPushButton):
    def __init__(self, label="", background="yellow"):
        super().__init__(label)
        self.setFixedHeight(55)
        # geometry
        style_sheet = "QPushButton{border-width:0px; border-radius:0px}"
        style_sheet += "QPushButton{font: bold}"
        # color
        style_sheet += "QPushButton{background: red}"
        self.setStyleSheet(style_sheet)
