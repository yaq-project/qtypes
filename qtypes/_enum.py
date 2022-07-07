__all__ = ["Enum"]


from typing import Any, Dict

from ._base import Base


class Enum(Base):
    qtype = "enum"

    def __init__(self, label: str = "", value="", allowed=[""], disabled=False):
        super().__init__(label=label, value=value, disabled=disabled)
        self._data["allowed"] = allowed

    def set(self, value: dict, *, from_widget=False):
        new_val = value.get("value", self._data["value"])
        allowed = value.get("allowed", self._data["allowed"])
        if not allowed:
            allowed = [""]
            value["allowed"] = allowed
        if new_val not in allowed:
            value["value"] = allowed[0]
        super().set(value, from_widget=from_widget)
