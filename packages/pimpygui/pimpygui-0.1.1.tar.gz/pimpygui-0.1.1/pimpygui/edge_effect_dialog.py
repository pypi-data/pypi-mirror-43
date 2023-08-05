import os

import numpy

from PySide2.QtGui import QPixmap
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QDialogButtonBox, QVBoxLayout, QWidget

from pimpy.transformations import create_edge_image
from pimpygui.effect_dialog import EffectDialog
from pimpygui.utils import array_to_qimage, qimage_to_array


_edge_effect_widget_ui_file_path = os.path.join(os.path.dirname(__file__), "ui", "edge_effect_widget.ui")


class EdgeEffectDialog(EffectDialog):

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Edge Effect")

        self.setLayout(QVBoxLayout(self))
        self.widget = QUiLoader().load(_edge_effect_widget_ui_file_path, self)
        self.layout().addWidget(self.widget)

        self._get_button_box().accepted.connect(self.accept)
        self._get_button_box().rejected.connect(self.reject)

    def set_input_pixmap(self, pixmap: QPixmap) -> None:
        img = qimage_to_array(pixmap.toImage())
        self._compute_edges(img)

    def _compute_edges(self, img: numpy.ndarray) -> None:
        """Computes the edge image and emits the update_image signal with the result."""
        edges = create_edge_image(img)
        edge_colors = numpy.array([[255, 255, 255], [0, 0, 0]], dtype=numpy.uint8)
        edge_img = edge_colors[edges]
        qimg = array_to_qimage(edge_img)
        self.update_image.emit(QPixmap(qimg))

    def _get_button_box(self) -> QDialogButtonBox:
        assert isinstance(self.widget.buttonBox, QDialogButtonBox)
        return self.widget.buttonBox
