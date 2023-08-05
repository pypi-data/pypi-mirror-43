from typing import Optional, Tuple

from PySide2.QtCore import Qt, QEvent, QObject, Signal
from PySide2.QtGui import QPixmap, QResizeEvent
from PySide2.QtWidgets import QLabel, QWidget


class ImageWidget(QWidget):
    """The ImageWidget is a QWidget that displays an image while keeping its aspect ratio."""

    _placeholder_text = "< image >"
    mouse_moved = Signal(int, int)
    mouse_pressed = Signal(int, int)

    def __init__(self, parent: QWidget = None) -> None:
        """Creates the widget and its children."""
        super().__init__(parent)
        self._label = QLabel(self)
        self._label.setScaledContents(True)
        self._label.setAlignment(Qt.AlignCenter)
        self._label.setMouseTracking(True)
        self._label.installEventFilter(self)
        self.clear()

    def set_pixmap(self, pixmap: QPixmap) -> None:
        """Stores and displays the given pixmap."""
        self._label.setPixmap(pixmap)
        self._resize_label()

    def get_pixmap(self) -> Optional[QPixmap]:
        """Returns the current pixmap, or None if no pixmap has been set."""
        return self._label.pixmap()

    def clear(self) -> None:
        """Removes the image and displays a placeholder text."""
        self._label.setText(ImageWidget._placeholder_text)

    def resizeEvent(self, event: QResizeEvent):
        """Calls _resize_label()."""
        self._resize_label()

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        """Emits the mouse_moved and mouse_pressed signals."""
        if watched == self._label:
            signal = None
            if event.type() == QEvent.MouseMove:
                signal = self.mouse_moved
            elif event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
                signal = self.mouse_pressed
            if signal and self._label.pixmap():
                try:
                    x, y = self._map_label_to_image_coords(event.pos().x(), event.pos().y())
                    signal.emit(x, y)
                except RuntimeError:
                    pass
        return super().eventFilter(watched, event)

    def _resize_label(self):
        """Resizes the label so that it displays the image as large as possible while keeping the aspect ratio."""
        widget_width = self.size().width()
        widget_height = self.size().height()
        if widget_width <= 0 or widget_height <= 0:
            return

        img = self._label.pixmap()
        if img:
            widget_ratio = widget_width / widget_height
            img_ratio = img.width() / img.height()
            if widget_ratio > img_ratio:
                img_height = widget_height
                img_width = img_ratio * img_height
            else:
                img_width = widget_width
                img_height = img_width / img_ratio
            img_x = (widget_width - img_width) // 2
            img_y = (widget_height - img_height) // 2
            self._label.setGeometry(img_x, img_y, img_width, img_height)
        else:
            self._label.setGeometry(0, 0, widget_width, widget_height)

    def _map_label_to_image_coords(self, label_x: int, label_y: int) -> Tuple[int, int]:
        """Converts the given label coordinates to image coordinates and returns the result."""
        assert self._label.pixmap()
        x = 0
        if self._label.width() > 0 and self._label.pixmap().width() > 0:
            x = int((label_x * self._label.pixmap().width()) / self._label.width())
        y = 0
        if self._label.height() > 0 and self._label.pixmap().height() > 0:
            y = int((label_y * self._label.pixmap().height()) / self._label.height())
        return x, y
