__all__ = ["Null"]


from typing import Any, Dict

from ._base import Base


class Null(Base):
    defaults: Dict[str, Any] = dict()
    defaults["value"] = None

    def _create_widget(self):
        return Widget()

    def on_updated(self, value: dict):
        pass
