__all__ = ["Button"]


from typing import Any, Dict

from ._base import Base


class Button(Base):
    defaults: Dict[str, Any] = dict()
    defaults["value"] = None
    defaults["background_color"] = None
    defaults["text"] = "button"
    defaults["text_color"] = None

    def _create_widget(self):
        self._widget = Widget(self._value["text"])
        self._widget.clicked.connect(self._on_clicked)
        return self._widget

    def _on_clicked(self):
        self.edited.emit(self._value)
        self.updated.emit(self._value)

    def on_updated(self, value):
        self._widget.setText(self._value["text"])
