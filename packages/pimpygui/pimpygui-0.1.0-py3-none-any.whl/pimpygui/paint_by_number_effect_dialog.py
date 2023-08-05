import os
from typing import Iterator, Tuple

import numpy

from PySide2.QtCore import QRect
from PySide2.QtGui import QColor, QFont, QImage, QPaintDevice, QPainter, QPen, QPixmap
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QDialogButtonBox, QFontDialog, QLabel, QLayout, QPushButton, QRadioButton, QVBoxLayout,\
    QWidget

from pimpy.color_cluster import extract_colors
from pimpy.transformations import create_edge_image, find_poles_of_inaccessibility_of_edge_image
from pimpygui.color_widget import ColorWidget
from pimpygui.effect_dialog import EffectDialog
from pimpygui.utils import array_to_qimage, qimage_to_array


_paint_by_number_effect_widget_ui_file_path = os.path.join(
    os.path.dirname(__file__), "ui", "paint_by_number_effect_widget.ui"
)


Point = Tuple[int, int]


class PaintByNumberEffectDialog(EffectDialog):

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Paint By Numbers Effect")

        self.setLayout(QVBoxLayout(self))
        self.widget = QUiLoader().load(_paint_by_number_effect_widget_ui_file_path, self)
        self.layout().addWidget(self.widget)

        self._color_widget = ColorWidget(self.widget)
        self._color_widget.set_color(QColor(255, 0, 0))
        self._color_widget.color_changed.connect(self._draw_labels_and_update_image)
        self._get_layout_color().addWidget(self._color_widget)

        self._get_button_box().accepted.connect(self.accept)
        self._get_button_box().rejected.connect(self.reject)
        self._get_button_choose_font().clicked.connect(self._show_choose_font_dialog)

        self._font = QFont()
        self._set_font(self._font)  # update the font label

        self._input_colors = None
        self._input_labels = None
        self._edge_qimg = None
        self._poles_of_inaccessibility = None
        self._labels_with_position = None

    def set_input_pixmap(self, pixmap: QPixmap) -> None:
        img = qimage_to_array(pixmap.toImage())
        self._input_colors, self._input_labels = extract_colors(img)
        edges = create_edge_image(img)
        self._poles_of_inaccessibility = find_poles_of_inaccessibility_of_edge_image(edges)
        edge_colors = numpy.array([[255, 255, 255], [0, 0, 0]], dtype=numpy.uint8)
        edge_img = edge_colors[edges]
        self._edge_qimg = array_to_qimage(edge_img)
        self._labels_with_position = list(self._yield_labels_of_poles_of_inaccessibility())
        self._draw_labels_and_update_image()

    def pixel_clicked(self, x: int, y: int) -> None:
        """Adds / removes a label at the clicked pixel, depending on the radio button states of the GUI."""
        if self._get_radio_button_add_label().isChecked():
            self._add_label(y, x)
        if self._get_radio_button_remove_label().isChecked():
            self._remove_label(y, x)

    def _add_label(self, x: int, y: int) -> None:
        """Adds a label at the given position."""
        p_input_img = (x//2, y//2)
        for pos, label in self._labels_with_position:
            if p_input_img == pos:
                return
        label = self._input_labels[p_input_img]
        self._labels_with_position.append(((x, y), label))
        self._draw_labels_and_update_image()

    def _remove_label(self, x: int, y: int) -> None:
        """Removes the label closest to the clicked position."""
        if not self._labels_with_position:
            return
        closest_distance_sq = (self._input_labels.shape[0]*2 + self._input_labels.shape[1]*2)**2
        closest_index = -1
        for i, ((px, py), _) in enumerate(self._labels_with_position):
            distance_sq = (x-px)**2 + (y-py)**2
            if distance_sq < closest_distance_sq:
                closest_distance_sq = distance_sq
                closest_index = i
        assert 0 <= closest_index < len(self._input_labels)
        self._labels_with_position.pop(closest_index)
        self._draw_labels_and_update_image()

    def _yield_labels_of_poles_of_inaccessibility(self) -> Iterator[Tuple[Point, int]]:
        """Yields tuples (position, label) with the position of each label using the poles of inaccessibility of the
        original edge image."""
        for p in self._poles_of_inaccessibility:
            p_input_img = (p[0]//2, p[1]//2)
            label = self._input_labels[p_input_img]
            yield p, label

    def _draw_labels_and_update_image(self) -> None:
        """Draws the current labels on the edge image and emits the update_image signal."""
        assert isinstance(self._edge_qimg, QImage)
        qimg = self._edge_qimg.copy()
        painter = self._create_painter_from_gui_settings(qimg)
        for pos, label in self._labels_with_position:
            text = str(label+1)  # programmers start counting at zero, but boring people start at one
            rect = painter.boundingRect(QRect(), 0, text)
            px = pos[1] - (rect.width() // 2)
            py = pos[0] - (rect.height() // 2)
            rect.translate(px, py)
            painter.drawText(rect, 0, text)
        painter.end()
        self.update_image.emit(QPixmap(qimg))

    def _create_painter_from_gui_settings(self, device: QPaintDevice) -> QPainter:
        """Returns a QPainter for the given device using the current settings from the GUI."""
        painter = QPainter(device)
        painter.setPen(QPen(self._color_widget.get_color()))
        painter.setFont(self._font)
        return painter

    def _show_choose_font_dialog(self) -> None:
        """Shows a dialog to choose the font and redraws the image with the result."""
        success, new_font = QFontDialog.getFont(self._font, self.widget)
        if success:
            self._set_font(new_font)
            self._draw_labels_and_update_image()

    def _set_font(self, font: QFont) -> None:
        """Sets the font and updates the font label accordingly."""
        self._font = font
        self._get_label_font().setFont(self._font)
        self._get_label_font().setText(self._font.family())

    def _get_button_box(self) -> QDialogButtonBox:
        assert isinstance(self.widget.buttonBox, QDialogButtonBox)
        return self.widget.buttonBox

    def _get_label_font(self) -> QLabel:
        assert isinstance(self.widget.labelFont, QLabel)
        return self.widget.labelFont

    def _get_button_choose_font(self) -> QPushButton:
        assert isinstance(self.widget.buttonChooseFont, QPushButton)
        return self.widget.buttonChooseFont

    def _get_layout_color(self) -> QLayout:
        assert isinstance(self.widget.layoutColor, QLayout)
        return self.widget.layoutColor

    def _get_radio_button_add_label(self) -> QRadioButton:
        assert isinstance(self.widget.radioButtonAddLabel, QRadioButton)
        return self.widget.radioButtonAddLabel

    def _get_radio_button_remove_label(self) -> QRadioButton:
        assert isinstance(self.widget.radioButtonRemoveLabel, QRadioButton)
        return self.widget.radioButtonRemoveLabel
