__all__ = ["Float"]


import math
from dataclasses import dataclass
from typing import Any, Dict

from ._base import Base
from ._units import converter, get_valid_conversions


class Float(Base):
    qtype = "float"

    def __init__(self, label: str = "", value=float("nan"), units=None, minimum=float("-inf"), maximum=float("+inf"), decimals=6, disabled=False):
        super().__init__(label=label, value=value, disabled=disabled)
        self._data["units"] = units
        self._data["minimum"] = minimum
        self._data["maximum"] = maximum
        self._data["decimals"] = decimals

    @property
    def allowed_units(self):
        out = []
        for i in range(self._widget.combo_box.count()):
            out.append(self._widget.combo_box.itemText(i))
        return out
