from qtpy import QtWidgets, QtGui, QtCore


class Widget(QtWidgets.QSpinBox):
    def __init__(self, model, parent):
        super().__init__(parent=parent)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.installEventFilter(self)
        self.editingFinished.connect(self.on_editing_finished)
        # wire into model
        self.model = model
        self.model.updated_connect(self.on_updated)
        self.on_updated(model.get())

    def eventFilter(self, obj, event):
        if isinstance(event, QtGui.QWheelEvent):
            return True
        else:
            return super().eventFilter(obj, event)

    def updated_disconnect(self):
        self.model.updated_disconnect(self.on_updated)

    def on_editing_finished(self):
        self.model.set({"value": self.value()}, from_widget=True)

    def on_updated(self, data):
        # minimum, maximum
        self.setMinimum(int(data["minimum"]))
        self.setMaximum(int(data["maximum"]))
        # tool tip
        self.setToolTip(f"minimum:{int(data['minimum'])}\nmaximum:{int(data['maximum'])}")
        if not self.hasFocus():
            self.setValue(data["value"])
            self.setDisabled(data["disabled"])
