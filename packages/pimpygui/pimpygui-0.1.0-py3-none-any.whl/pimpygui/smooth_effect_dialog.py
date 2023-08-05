import os

import numpy

from PySide2.QtGui import QPixmap
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QDialogButtonBox, QDoubleSpinBox, QVBoxLayout, QWidget

from pimpy.smoothing import gaussian_smoothing
from pimpygui.effect_dialog import EffectDialog
from pimpygui.utils import array_to_qimage, qimage_to_array


_smooth_effect_dialog_widget_ui_file_path = os.path.join(os.path.dirname(__file__), "ui", "smooth_effect_widget.ui")


class SmoothEffectDialog(EffectDialog):

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Smooth Effect")
        self._input_array = None

        self.setLayout(QVBoxLayout(self))
        self.widget = QUiLoader().load(_smooth_effect_dialog_widget_ui_file_path, self)
        self.layout().addWidget(self.widget)

        self._get_button_box().accepted.connect(self.accept)
        self._get_button_box().rejected.connect(self.reject)
        self._get_spinbox_sigma().valueChanged.connect(self._compute_smoothing)

    def _get_spinbox_sigma(self) -> QDoubleSpinBox:
        assert isinstance(self.widget.spinBoxSigma, QDoubleSpinBox)
        return self.widget.spinBoxSigma

    def _get_sigma(self) -> float:
        return self._get_spinbox_sigma().value()

    def _get_button_box(self) -> QDialogButtonBox:
        assert isinstance(self.widget.buttonBox, QDialogButtonBox)
        return self.widget.buttonBox

    def set_input_pixmap(self, pixmap: QPixmap) -> None:
        self._input_array = qimage_to_array(pixmap.toImage())
        self._compute_smoothing()

    def _compute_smoothing(self) -> None:
        """Applies a gaussian soothing and emits the update_image signal with the result."""
        assert isinstance(self._input_array, numpy.ndarray)
        img = gaussian_smoothing(self._input_array, self._get_sigma())
        qimg = array_to_qimage(img)
        self.update_image.emit(QPixmap(qimg))
