import unittest

import numpy
from PySide2.QtGui import QColor, QImage

from pimpygui.utils import array_to_qimage, qimage_to_array


def _create_test_qimage():
    img = QImage(4, 2, QImage.Format_RGB888)
    img.setPixelColor(0, 0, QColor(0, 0, 1))
    img.setPixelColor(0, 1, QColor(3, 4, 5))
    img.setPixelColor(1, 0, QColor(0, 1, 2))
    img.setPixelColor(1, 1, QColor(4, 5, 6))
    img.setPixelColor(2, 0, QColor(1, 2, 3))
    img.setPixelColor(2, 1, QColor(5, 6, 7))
    img.setPixelColor(3, 0, QColor(2, 3, 4))
    img.setPixelColor(3, 1, QColor(6, 7, 8))
    return img


_img_array = numpy.array([
    [[0, 0, 1], [0, 1, 2], [1, 2, 3], [2, 3, 4]],
    [[3, 4, 5], [4, 5, 6], [5, 6, 7], [6, 7, 8]]
], dtype=numpy.uint8)

_img_qimage = _create_test_qimage()


class TestArrayToQImage(unittest.TestCase):

    def test_convert_simple_array(self):
        qimg = array_to_qimage(_img_array)
        self.assertEqual(qimg, _img_qimage)


class TestQImageToArray(unittest.TestCase):

    def test_convert_simple_array(self):
        arr = qimage_to_array(_img_qimage)
        self.assertTrue(numpy.array_equal(arr, _img_array))
