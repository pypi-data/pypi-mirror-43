import numpy

from PySide2.QtGui import QImage


def qimage_to_array(img: QImage) -> numpy.ndarray:
    """Converts the given QImage to a numpy array and returns it."""
    img = img.convertToFormat(QImage.Format_RGB888)
    buffer = numpy.array(img.constBits())
    shape = (img.height(), img.width(), 3)
    strides = (img.bytesPerLine(), 3, 1)
    return numpy.lib.stride_tricks.as_strided(buffer, shape, strides)


def array_to_qimage(arr: numpy.ndarray, copy: bool = True) -> QImage:
    """Converts the given numpy array to a QImage and returns it."""
    assert len(arr.shape) == 3
    assert arr.shape[-1] == 3
    assert arr.dtype == numpy.uint8
    qimg = QImage(arr.data, arr.shape[1], arr.shape[0], arr.strides[0], QImage.Format_RGB888)
    if copy:
        return qimg.copy()
    return qimg
