"""Input table."""


# --- import --------------------------------------------------------------------------------------

import os
import collections

from qtpy import QtWidgets, QtGui

from ..core.ini import INI

# --- class ---------------------------------------------------------------------------------------


here = os.path.abspath(os.path.dirname(__file__))

colors = INI(os.path.join(here, "colors.ini")).dictionary["night"]


class InputTable(QtWidgets.QWidget):
    def __init__(self, width_input=150):
        super().__init__()
        self.width_input = width_input
        self.setLayout(QtWidgets.QGridLayout())
        self.layout().setColumnMinimumWidth(0, 150)
        self.layout().setColumnMinimumWidth(1, 150)
        self.layout().setMargin(0)
        self.row_number = 0
        self.controls = []
        self._dict = collections.OrderedDict()

    def add(self, name, global_object, key=None):
        if key is None:
            key = name
        if global_object is None:
            global_type = "heading"
        else:
            global_type = global_object.type
            self._dict[key] = global_object
        getattr(self, global_type)(name, global_object)

    def heading(self, name, global_object):
        # heading
        heading = QtWidgets.QLabel(name)
        StyleSheet = "QLabel{color: custom_color; font: bold 14px;}".replace(
            "custom_color", colors["foreground"]
        )
        heading.setStyleSheet(StyleSheet)
        heading.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        self.layout().addWidget(heading, self.row_number, 0)
        self.controls.append(None)
        self.row_number += 1

    def number(self, name, global_object):
        # heading
        heading = QtWidgets.QLabel(name)
        StyleSheet = "QLabel{color: custom_color; font: 14px;}".replace(
            "custom_color", colors["foreground"]
        )
        heading.setStyleSheet(StyleSheet)
        heading.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        self.layout().addWidget(heading, self.row_number, 0)
        # layout
        container_widget = QtWidgets.QWidget()
        container_widget.setLayout(QtWidgets.QHBoxLayout())
        layout = container_widget.layout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        # control
        control = QtWidgets.QDoubleSpinBox()
        if global_object.display:
            control.setDisabled(True)
            StyleSheet = "QDoubleSpinBox{color: custom_color_1; font: bold font_sizepx; border: 0px solid #000000;}".replace(
                "custom_color_1", g.colors_dict.read()["text_light"]
            ).replace(
                "font_size", str(int(14))
            )
            StyleSheet += "QScrollArea, QWidget{background: custom_color;  border-color: black;}".replace(
                "custom_color", g.colors_dict.read()["background"]
            )
        else:
            StyleSheet = "QDoubleSpinBox{color: custom_color; font: 14px;}".replace(
                "custom_color", colors["foreground"]
            )
            StyleSheet += "QScrollArea, QWidget{color: custom_color_1; border: 1px solid custom_color_2; border-radius: 1px;}".replace(
                "custom_color_1", colors["foreground"]
            ).replace(
                "custom_color_2", colors["background"]
            )
            StyleSheet += "QWidget:disabled{color: custom_color_1; font: 14px; border: 1px solid custom_color_2; border-radius: 1px;}".replace(
                "custom_color_1", colors["comment"]
            ).replace(
                "custom_color_2", colors["background"]
            )
        control.setStyleSheet(StyleSheet)
        control.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        global_object.give_control(control)
        layout.addWidget(control)
        # units combobox
        if not global_object.units_kind == None:
            control.setMinimumWidth(self.width_input - 55)
            control.setMaximumWidth(self.width_input - 55)
            units = QtWidgets.QComboBox()
            units.setMinimumWidth(50)
            units.setMaximumWidth(50)
            StyleSheet = "QComboBox{color: custom_color_1; font: 14px; border: 1px solid custom_color_2; border-radius: 1px;}".replace(
                "custom_color_1", colors["foreground"]
            ).replace(
                "custom_color_2", colors["background"]
            )
            StyleSheet += "QComboBox:disabled{color: custom_color_1; font: 14px; border: 1px solid custom_color_2; border-radius: 1px;}".replace(
                "custom_color_1", colors["comment"]
            ).replace(
                "custom_color_2", colors["background"]
            )
            StyleSheet += "QAbstractItemView{color: custom_color_1; font: 50px solid white;}".replace(
                "custom_color_1", colors["foreground"]
            ).replace(
                "custom_color_2", colors["background"]
            )
            units.setStyleSheet(StyleSheet)
            layout.addWidget(units)
            global_object.give_units_combo(units)
        # finish
        self.layout().addWidget(container_widget, self.row_number, 1)
        self.controls.append(container_widget)
        self.row_number += 1

    def string(self, name, global_object):
        # heading
        heading = QtWidgets.QLabel(name)
        heading.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        StyleSheet = "QLabel{color: custom_color; font: 14px;}".replace(
            "custom_color", colors["foreground"]
        )
        heading.setStyleSheet(StyleSheet)
        self.layout().addWidget(heading, self.row_number, 0)
        # control
        control = QtWidgets.QLineEdit()
        control.setMinimumWidth(self.width_input)
        control.setMaximumWidth(self.width_input)
        if global_object.display:
            control.setDisabled(True)
            StyleSheet = "QWidget{color: custom_color_1; font: bold 14px; border: 0px solid custom_color_2; border-radius: 1px;}".replace(
                "custom_color_1", colors["foreground"]
            ).replace(
                "custom_color_2", colors["background"]
            )
        else:
            StyleSheet = "QWidget{color: custom_color_1; font: 14px; border: 1px solid custom_color_2; border-radius: 1px;}".replace(
                "custom_color_1", colors["foreground"]
            ).replace(
                "custom_color_2", colors["background"]
            )
            StyleSheet += "QWidget:disabled{color: custom_color_1; font: 14px; border: 1px solid custom_color_2; border-radius: 1px;}".replace(
                "custom_color_1", colors["text_disabled"]
            ).replace(
                "custom_color_2", colors["widget_background"]
            )
        control.setStyleSheet(StyleSheet)
        global_object.give_control(control)
        # finish
        self.layout().addWidget(control, self.row_number, 1)
        self.controls.append(control)
        self.row_number += 1

    def combo(self, name, global_object):
        # heading
        heading = QtWidgets.QLabel(name)
        heading.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        StyleSheet = "QLabel{color: custom_color; font: 14px;}".replace(
            "custom_color", colors["foreground"]
        )
        heading.setStyleSheet(StyleSheet)
        self.layout().addWidget(heading, self.row_number, 0)
        # control
        control = QtWidgets.QComboBox()
        control.setMinimumWidth(self.width_input)
        control.setMaximumWidth(self.width_input)
        if global_object.display:
            control.setDisabled(True)
            StyleSheet = "QComboBox{color: custom_color_1; font: bold 14px; border: 0px solid custom_color_2; border-radius: 1px;}".replace(
                "custom_color_1", colors["foreground"]
            ).replace(
                "custom_color_2", colors["widget_background"]
            )
            # StyleSheet += 'QComboBox:disabled{color: custom_color_1; font: 14px; border: 0px solid custom_color_2; border-radius: 1px;}'.replace('custom_color_1', colors['text_disabled']).replace('custom_color_2', colors['widget_background'])
            StyleSheet += "QAbstractItemView{color: custom_color_1; font: 50px solid white; border: 0px white}".replace(
                "custom_color_1", colors["background"]
            ).replace(
                "custom_color_2", colors["background"]
            )
            StyleSheet += "QComboBox::drop-down{border: 0;}"
        else:
            StyleSheet = "QComboBox{color: custom_color_1; font: 14px; border: 1px solid custom_color_2; border-radius: 1px;}".replace(
                "custom_color_1", colors["foreground"]
            ).replace(
                "custom_color_2", colors["background"]
            )
            StyleSheet += "QComboBox:disabled{color: custom_color_1; font: 14px; border: 1px solid custom_color_2; border-radius: 1px;}".replace(
                "custom_color_1", colors["comment"]
            ).replace(
                "custom_color_2", colors["background"]
            )
            StyleSheet += "QAbstractItemView{color: custom_color_1; font: 50px solid white;}".replace(
                "custom_color_1", colors["foreground"]
            ).replace(
                "custom_color_2", colors["background"]
            )
        control.setStyleSheet(StyleSheet)
        global_object.give_control(control)
        # finish
        self.layout().addWidget(control, self.row_number, 1)
        self.controls.append(control)
        self.row_number += 1

    def checkbox(self, name, global_object):
        raise NotImplementedError
        # heading
        heading = QtWidgets.QLabel(name)
        heading.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        StyleSheet = "QLabel{color: custom_color; font: 14px;}".replace(
            "custom_color", colors[foreground]
        )
        heading.setStyleSheet(StyleSheet)
        self.layout().addWidget(heading, self.row_number, 0)
        # control
        if global_object.display:
            control = Led()
        else:
            control = QtWidgets.QCheckBox()
        global_object.give_control(control)
        # finish
        self.layout().addWidget(control, self.row_number, 1)
        self.controls.append(control)
        self.row_number += 1

    def filepath(self, name, global_object):
        raise NotImplementedError
        # heading
        heading = QtWidgets.QLabel(name)
        heading.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        StyleSheet = "QLabel{color: custom_color; font: 14px;}".replace(
            "custom_color", colors[foreground]
        )
        heading.setStyleSheet(StyleSheet)
        self.layout().addWidget(heading, self.row_number, 0)
        # layout
        container_widget = QtWidgets.QWidget()
        container_widget.setLayout(QtWidgets.QHBoxLayout())
        layout = container_widget.layout()
        layout.setMargin(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        # push button
        load_button = QtWidgets.QPushButton("Load")
        StyleSheet = "QPushButton{background:custom_color; border-width:0px;  border-radius: 0px; font: bold 14px}".replace(
            "custom_color", colors["go"]
        )
        load_button.setStyleSheet(StyleSheet)
        load_button.setMinimumHeight(20)
        load_button.setMaximumHeight(20)
        load_button.setMinimumWidth(40)
        load_button.setMaximumWidth(40)
        layout.addWidget(load_button)
        global_object.give_button(load_button)
        # display
        display = QtWidgets.QLineEdit()
        # display.setDisabled(True)
        display.setReadOnly(True)
        display.setMinimumWidth(self.width_input - 45)
        display.setMaximumWidth(self.width_input - 45)
        StyleSheet = "QWidget{color: custom_color_1; font: 14px; border: 1px solid custom_color_2; border-radius: 1px;}".replace(
            "custom_color_1", colors["foreground"]
        ).replace(
            "custom_color_2", colors["widget_background"]
        )
        StyleSheet += "QWidget:disabled{color: custom_color_1; font: 14px; border: 1px solid custom_color_2; border-radius: 1px;}".replace(
            "custom_color_1", colors["text_disabled"]
        ).replace(
            "custom_color_2", colors["widget_background"]
        )
        display.setStyleSheet(StyleSheet)
        layout.addWidget(display)
        global_object.give_control(display)
        # finish
        self.layout().addWidget(container_widget, self.row_number, 1)
        self.controls.append(container_widget)
        self.row_number += 1
