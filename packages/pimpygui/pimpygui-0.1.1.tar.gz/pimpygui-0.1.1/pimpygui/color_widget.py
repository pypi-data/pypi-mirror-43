from PySide2.QtCore import Signal
from PySide2.QtGui import QColor, QPalette
from PySide2.QtWidgets import QColorDialog, QFrame, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QWidget


class ColorWidget(QWidget):
    """The ColorWidget displays a color rectangle and a button that shows a color dialog to change the color."""

    color_changed = Signal(QColor)

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self._color_label = QLabel(self)
        self._color_label.setAutoFillBackground(True)
        self._color_label.setFrameShape(QFrame.Box)
        self._color_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(self._color_label)
        self._button = QPushButton("Edit", self)
        self._button.clicked.connect(self._show_edit_color_dialog)
        layout.addWidget(self._button)

        self._color = QColor(0, 0, 0)
        self.set_color(self._color)

    def set_color(self, color: QColor) -> None:
        """Sets the displayed color. This does not emit the color_changed signal."""
        self._color = color
        palette = self._color_label.palette()
        palette.setColor(QPalette.Window, color)
        self._color_label.setPalette(palette)

    def get_color(self) -> QColor:
        """Returns the current color."""
        return self._color

    def _show_edit_color_dialog(self) -> None:
        """Shows a dialog in which the user can change the color and emits the color_changed signal."""
        color = QColorDialog.getColor(self._color)
        if color.isValid():
            self.set_color(color)
            self.color_changed.emit(color)
