from qtpy import QtWidgets, QtGui, QtCore


class Widget(QtWidgets.QLineEdit):
    def __init__(self, model, parent):
        super().__init__(parent=parent)
        # wire into model
        self.model = model
        self.model.updated_connect(self.on_updated)
        self.on_updated(model.get())

    def on_updated(self, value):
        self.setText(value["value"])
