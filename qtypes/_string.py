from ._mobject import MObject


class String(MObject):
    def __init__(self, initial_value="", max_length=None, *args, **kwargs):
        super().__init__(initial_value=initial_value, *args, **kwargs)
        self.type = "string"
        self.max_length = max_length

    def give_control(self, control_widget):
        self.widget = control_widget
        if self.max_length is not None:
            self.widget.setMaxLength(self.max_length)
        # fill out items
        self.widget.setText(str(self.value.read()))
        # connect signals and slots
        self.updated.connect(lambda: self.widget.setText(self.value.read()))
        self.widget.editingFinished.connect(lambda: self.write(str(self.widget.text())))
        self.widget.setToolTip(self.tool_tip)
        self.has_widget = True

    def read(self):
        return str(PyCMDS_Object.read(self))

    def write(self, value):
        if self.max_length is not None:
            value = value[: self.max_length]
        self.value.write(value)
        self.updated.emit()
