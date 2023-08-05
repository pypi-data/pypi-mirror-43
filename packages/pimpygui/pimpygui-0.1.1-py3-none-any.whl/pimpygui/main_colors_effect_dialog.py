import os

import numpy

from PySide2.QtGui import QColor, QPixmap
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QDialogButtonBox, QLayout, QPushButton, QSpinBox, QVBoxLayout, QWidget

from pimpy.color_cluster import find_nearest_colors, reduce_image
from pimpygui.color_widget import ColorWidget
from pimpygui.effect_dialog import EffectDialog
from pimpygui.utils import array_to_qimage, qimage_to_array


_main_colors_effect_widget_ui_file_path = os.path.join(os.path.dirname(__file__), "ui", "main_colors_effect_widget.ui")


class MainColorsEffectDialog(EffectDialog):

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Main Colors Effect")
        self._input_array = None

        self.setLayout(QVBoxLayout(self))
        self.widget = QUiLoader().load(_main_colors_effect_widget_ui_file_path, self)
        self.layout().addWidget(self.widget)

        self._current_colors = numpy.zeros((self._get_number_of_colors(), 3))
        self._color_widgets = []

        self._get_spinbox_number_of_colors().valueChanged.connect(self._on_spinbox_value_changed)
        self._get_button_automatic_colors().clicked.connect(self._on_button_automatic_colors_clicked)
        self._get_button_box().accepted.connect(self.accept)
        self._get_button_box().rejected.connect(self.reject)

        self._update_color_widgets_from_current_colors()

    def set_input_pixmap(self, pixmap: QPixmap) -> None:
        """Stores the given image, computes its main colors, and updates the widgets accordingly."""
        self._input_array = qimage_to_array(pixmap.toImage())
        self._current_colors = self._find_main_colors()
        self._update_color_widgets_from_current_colors()
        self._update_image_from_current_colors()

    def _find_main_colors(self) -> numpy.ndarray:
        """Computes the main colors of the input image and returns them."""
        assert isinstance(self._input_array, numpy.ndarray)
        return reduce_image(self._input_array, self._get_number_of_colors())[0]

    def _update_color_widgets_from_current_colors(self) -> None:
        """Adds / removes color widgets until their number matches the current colors array and sets their colors."""
        # Add / remove the widgets so that their number is correct.
        num_colors = self._get_number_of_colors()
        assert isinstance(self._current_colors, numpy.ndarray)
        assert len(self._current_colors.shape) == 2
        assert self._current_colors.shape[0] >= num_colors
        while len(self._color_widgets) < num_colors:
            w = ColorWidget(self.widget)
            self._get_layout_colors().addWidget(w)
            w.color_changed.connect(self._on_widget_color_changed)
            self._color_widgets.append(w)
        while len(self._color_widgets) > num_colors:
            w = self._color_widgets.pop()
            assert isinstance(w, ColorWidget)
            w.deleteLater()

        # Update the widget colors.
        for i in range(num_colors):
            w = self._color_widgets[i]
            assert isinstance(w, ColorWidget)
            c = self._current_colors[i]
            w.set_color(QColor(c[0], c[1], c[2]))

    def _update_image_from_current_colors(self) -> None:
        """Recomputes the image using the current colors and emits the update_image signal."""
        assert isinstance(self._input_array, numpy.ndarray)
        assert self._get_number_of_colors() <= self._current_colors.shape[0]
        colors = self._current_colors[:self._get_number_of_colors()]
        labels = find_nearest_colors(self._input_array, colors)
        img = colors[labels]
        qimg = array_to_qimage(img)
        self.update_image.emit(QPixmap(qimg))

    def _update_current_colors_from_color_widgets(self) -> None:
        """Reads and stores the current colors from the widgets."""
        assert len(self._current_colors.shape) == 2
        assert self._current_colors.shape[0] >= len(self._color_widgets)
        for i, widget in enumerate(self._color_widgets):
            assert isinstance(widget, ColorWidget)
            color = widget.get_color()
            self._current_colors[i] = [color.red(), color.green(), color.blue()]

    def _on_spinbox_value_changed(self) -> None:
        """Enlarges the current color array (if necessary) and updates the color widgets and the image."""
        assert len(self._current_colors.shape) == 2
        assert self._current_colors.shape[0] > 0
        assert self._current_colors.shape[1] > 0
        num_requested_colors = self._get_number_of_colors()
        num_available_colors = self._current_colors.shape[0]
        if num_available_colors < num_requested_colors:
            self._current_colors.resize((num_requested_colors, self._current_colors.shape[1]))
            for i in range(num_available_colors, num_requested_colors):
                self._current_colors[i] = self._current_colors[i-1]
        self._update_color_widgets_from_current_colors()
        self._update_image_from_current_colors()

    def _on_button_automatic_colors_clicked(self) -> None:
        """Finds the main colors of the input image and updates the color widgets and the image accordingly."""
        self._current_colors = self._find_main_colors()
        self._update_color_widgets_from_current_colors()
        self._update_image_from_current_colors()

    def _on_widget_color_changed(self) -> None:
        """Updates the current colors from the widget and updates the image."""
        self._update_current_colors_from_color_widgets()
        self._update_image_from_current_colors()

    def _get_layout_colors(self) -> QLayout:
        assert isinstance(self.widget.layoutColors, QLayout)
        return self.widget.layoutColors

    def _get_button_automatic_colors(self) -> QPushButton:
        assert isinstance(self.widget.buttonAutomaticColors, QPushButton)
        return self.widget.buttonAutomaticColors

    def _get_spinbox_number_of_colors(self) -> QSpinBox:
        assert isinstance(self.widget.spinBoxNumberOfColors, QSpinBox)
        return self.widget.spinBoxNumberOfColors

    def _get_number_of_colors(self) -> int:
        return self._get_spinbox_number_of_colors().value()

    def _get_button_box(self) -> QDialogButtonBox:
        assert isinstance(self.widget.buttonBox, QDialogButtonBox)
        return self.widget.buttonBox
