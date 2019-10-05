"""Basic thread-safe data-containing object."""


import qtpy
from qtpy import QtCore, QtGui, QtWidgets


class Value(QtCore.QMutex):
    def __init__(self, initial_value=None):
        QtCore.QMutex.__init__(self)
        self.value = initial_value

    def read(self):
        return self.value

    def write(self, value):
        self.lock()
        self.value = value
        self.unlock()


class MObject(QtCore.QObject):
    updated = QtCore.Signal()
    disabled = False

    def __init__(
        self,
        initial_value=None,
        ini=None,
        section="",
        option="",
        import_from_ini=True,
        save_to_ini_at_shutdown=True,
        display=False,
        name="",
        label="",
        set_method=None,
        disable_under_queue_control=False,
        *args,
        **kwargs
    ):
        super().__init__()
        #
        self.has_widget = False
        self.tool_tip = ""
        self.value = Value(initial_value)
        self.display = display
        self.set_method = set_method
        if self.display:
            self.disabled = True
        else:
            self.disabled = False
        # ini
        if ini:
            self.has_ini = True
            self.ini = ini
            self.section = section
            self.option = option
        else:
            self.has_ini = False
        if import_from_ini:
            self.get_saved()
        # name
        self.name = name
        if not label == "":
            pass
        else:
            self.label = self.name

    def associate(self, display=None, pre_name=""):
        # display
        if display is None:
            display = self.display
        # name
        name = pre_name + self.name
        # new object
        new_obj = self.__class__(initial_value=self.read(), display=display, name=name)
        return new_obj

    def on_queue_control(self):
        if g.queue_control.read():
            if self.has_widget:
                self.widget.setDisabled(True)
        else:
            if self.has_widget:
                self.widget.setDisabled(self.disabled)

    def read(self):
        return self.value.read()

    def write(self, value):
        self.value.write(value)
        self.updated.emit()

    def get_saved(self):
        if self.has_ini:
            self.value.write(self.ini.read(self.section, self.option))
        self.updated.emit()

    def save(self, value=None):
        if value is not None:
            self.value.write(value)
        if self.has_ini:
            self.ini.write(self.section, self.option, self.value.read())

    def set_disabled(self, disabled):
        self.disabled = bool(disabled)
        if self.has_widget:
            self.widget.setDisabled(self.disabled)

    def setDisabled(self, disabled):
        self.set_disabled(disabled)

    def set_tool_tip(self, tool_tip):
        self.tool_tip = str(tool_tip)
        if self.has_widget:
            self.widget.setToolTip(self.tool_tip)
