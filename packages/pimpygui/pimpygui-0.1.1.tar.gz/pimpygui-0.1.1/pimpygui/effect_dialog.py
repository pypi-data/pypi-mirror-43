from PySide2.QtCore import Signal
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QDialog


class EffectDialog(QDialog):

    update_image = Signal(QPixmap)

    def set_input_pixmap(self, pixmap: QPixmap) -> None:
        """Sets the pixmap that is used as input for the effect."""
        raise NotImplementedError()

    def pixel_hovered(self, x: int, y: int) -> None:
        """Slot for pixel hover events."""
        pass

    def pixel_clicked(self, x: int, y: int) -> None:
        """Slot for pixel click events."""
        pass
