"""Thread-safe container for bool type."""


import qtpy
from qtpy import QtCore, QtGui, QtWidgets

from .mobject import MObject


class Bool(MObject):
    """
    holds 'value' (bool) - the state of the checkbox
    use read method to access
    """

    def __init__(self, initial_value=False, *args, **kwargs):
        super().__init__(initial_value=initial_value, *args, **kwargs)
        self.type = "checkbox"

    def give_control(self, control_widget):
        self.widget = control_widget
        # set
        self.widget.setChecked(self.value.read())
        # connect signals and slots
        self.updated.connect(lambda: self.widget.setChecked(self.value.read()))
        self.widget.stateChanged.connect(lambda: self.write(self.widget.isChecked()))
        # finish
        self.widget.setToolTip(self.tool_tip)
        self.widget.setDisabled(self.disabled)
        self.has_widget = True
