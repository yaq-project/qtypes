import math

from qtpy import QtWidgets, QtGui, QtCore

from .._units import converter, get_valid_conversions


class Widget(QtWidgets.QWidget):
    def __init__(self, model, parent):
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
        self.spin_box.editingFinished.connect(self.on_edited)
        self.combo_box.currentIndexChanged.connect(self.on_combo_changed)
        # wire into model
        self.model = model
        self.model.updated_connect(self.on_updated)
        self.on_updated(model.get())

    @property
    def allowed_units(self):
        out = []
        for i in range(self.combo_box.count()):
            out.append(self.combo_box.itemText(i))
        return out

    def on_combo_changed(self):
        new = self.combo_box.currentText()
        self.model.set({"units": new})

    def on_edited(self, value):
        pass

    def on_updated(self, value):
        """
        Must recieve complete and self-consistent dictionary.
        Updates state of widget
        """
        # units
        if value["units"] is not None and len(self.allowed_units) == 0:
            self.combo_box.currentIndexChanged.disconnect(self.on_combo_changed)
            self.combo_box.addItems(get_valid_conversions(value["units"]))
            self.combo_box.currentIndexChanged.connect(self.on_combo_changed)
        if value["units"] is not None:
            self.combo_box.show()
            self.combo_box.currentIndexChanged.disconnect(self.on_combo_changed)
            self.combo_box.setCurrentIndex(self.allowed_units.index(value["units"]))
            self.combo_box.currentIndexChanged.connect(self.on_combo_changed)
        # minimum, maximum
        data = self.model.get()
        self.spin_box.setMinimum(data["minimum"])
        self.spin_box.setMaximum(data["maximum"])
        # tool tip
        self.spin_box.setToolTip(f"minimum:{value['minimum']}\nmaximum:{value['maximum']}")
        if not self.spin_box.hasFocus():
            # decimals
            self.spin_box.setDecimals(data["decimals"])
            # value
            if math.isnan(value["value"]):
                self.spin_box.setSpecialValueText("nan")
                self.spin_box.setValue(self.spin_box.minimum())
            else:
                self.spin_box.setSpecialValueText("")
                self.spin_box.setValue(value["value"])
