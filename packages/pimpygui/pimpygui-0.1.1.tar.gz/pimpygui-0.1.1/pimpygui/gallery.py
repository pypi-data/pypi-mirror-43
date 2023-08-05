import argparse
from functools import partial
import logging
import os
import sys

from PySide2.QtCore import Qt
from PySide2.QtGui import QImageWriter, QPixmap
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QAction, QApplication, QFileDialog, QGroupBox, QLayout, QMainWindow, QMessageBox,\
    QPushButton, QWidget

from pimpygui.edge_effect_dialog import EdgeEffectDialog
from pimpygui.effect_dialog import EffectDialog
from pimpygui.history_stack import HistoryStack
from pimpygui.image_widget import ImageWidget
from pimpygui.main_colors_effect_dialog import MainColorsEffectDialog
from pimpygui.paint_by_number_effect_dialog import PaintByNumberEffectDialog
from pimpygui.smooth_effect_dialog import SmoothEffectDialog


_logger = logging.getLogger(__name__)
_gallery_ui_file_path = os.path.join(os.path.dirname(__file__), "ui", "gallery.ui")


class Gallery(object):
    def __init__(self, parent: QWidget = None) -> None:
        """Creates the gallery widgets."""
        loader = QUiLoader()
        self.widget = loader.load(_gallery_ui_file_path, parent)
        self.widget.setWindowTitle("pimpy gallery")
        self._image_widget = ImageWidget(self.widget)
        self._get_layout_current_image().addWidget(self._image_widget)
        self._history = HistoryStack()
        self._get_action_open_file().triggered.connect(self.show_load_image_dialog)
        self._get_action_save_file().triggered.connect(self.show_save_dialog)
        self._get_action_quit().triggered.connect(self.show_quit_dialog)
        self._get_action_undo().triggered.connect(self.perform_undo)
        self._get_action_redo().triggered.connect(self.perform_redo)
        self._current_effect_dialog = None
        self._current_image_before_effect = None

    def add_effect_dialog(self, button_text: str, effect_dialog_class) -> None:
        """Adds a button with the given text that shows the given effect dialog."""
        assert issubclass(effect_dialog_class, EffectDialog)
        btn = QPushButton(button_text, self.widget)
        btn.clicked.connect(partial(self._show_effect_dialog, effect_dialog_class))
        self._get_layout_effects().addWidget(btn)

    def show_load_image_dialog(self) -> None:
        """Shows a file dialog to get an existing file from the user and tries to load it."""
        dialog = QFileDialog(self.widget)
        image_mime_types = [m.data().decode() for m in QImageWriter().supportedMimeTypes()]
        image_mime_types.insert(0, "application/octet-stream")  # "All files (*)"
        dialog.setMimeTypeFilters(image_mime_types)
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        if dialog.exec_() == QFileDialog.Accepted:
            assert len(dialog.selectedFiles()) == 1
            file_path = dialog.selectedFiles()[0]
            self.load_image(file_path)

    def load_image(self, file_path: str) -> None:
        """Clears the current image and loads a new image from the specified path."""
        self.clear_current_image()
        img = QPixmap()
        if not img.load(file_path):
            _logger.warning("Failed to load image from file: \"{}\"".format(file_path))
            QMessageBox.warning(self.widget, "Error", "Failed to load image from file.")
        self.set_current_image(img)
        self.add_image_to_history(img)

    def show_save_dialog(self) -> None:
        """Shows a file dialog to save the current image file."""
        assert self.get_current_image()
        dialog = QFileDialog(self.widget)
        image_mime_types = [m.data().decode() for m in QImageWriter().supportedMimeTypes()]
        dialog.setMimeTypeFilters(image_mime_types)
        dialog.selectMimeTypeFilter("image/jpeg")
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        if dialog.exec_() == QFileDialog.Accepted:
            assert len(dialog.selectedFiles()) == 1
            file_path = dialog.selectedFiles()[0]
            mime_type = dialog.selectedMimeTypeFilter()
            available_formats = QImageWriter.imageFormatsForMimeType(mime_type.encode())
            assert available_formats
            self.save_current_image(file_path, available_formats[0].data().decode())

    def save_current_image(self, path: str, fmt: str) -> None:
        """Saves the current image at the specified path using the given format."""
        img = self.get_current_image()
        assert img
        result = img.save(path, fmt)
        if not result:
            QMessageBox.warning(self.widget, "Error", "Failed to save image.")

    def show_quit_dialog(self) -> None:
        """Shows a dialog that asks the user whether the application should be quit."""
        result = QMessageBox.question(self.widget, "Quit?", "Do you want to exit the application?")
        if result == QMessageBox.Yes:
            QApplication.quit()

    def clear_current_image(self) -> None:
        """Clears the current image. This does not effect the image history."""
        self._image_widget.clear()
        self._get_group_box_effects().setEnabled(False)
        self._get_action_save_file().setEnabled(False)

    def set_current_image(self, image: QPixmap) -> None:
        """Displays the given image. This does not effect the image history."""
        self._image_widget.set_pixmap(image)
        self._get_group_box_effects().setEnabled(True)
        self._get_action_save_file().setEnabled(True)

    def get_current_image(self) -> QPixmap:
        """Returns the current image of the image widget."""
        return self._image_widget.get_pixmap()

    def perform_undo(self) -> None:
        """Performs an undo step."""
        if self._history.can_go_backwards():
            self._history.go_backwards()
            img = self._history.get()
            if img is None:
                self.clear_current_image()
            else:
                assert isinstance(img, QPixmap)
                self.set_current_image(img)
        self._update_history_action()

    def perform_redo(self) -> None:
        """Performs a redo step."""
        if self._history.can_go_forwards():
            self._history.go_forwards()
            img = self._history.get()
            if img is None:
                self.clear_current_image()
            else:
                assert isinstance(img, QPixmap)
                self.set_current_image(img)
        self._update_history_action()

    def add_image_to_history(self, img: QPixmap) -> None:
        """Adds the current image to the image history."""
        self._history.add(img.copy())
        self._update_history_action()

    def _update_history_action(self) -> None:
        """Enables / Disables the undo / redo actions according to the current image history."""
        self._get_action_undo().setEnabled(self._history.can_go_backwards())
        self._get_action_redo().setEnabled(self._history.can_go_forwards())

    def _show_effect_dialog(self, cls) -> None:
        """Shows an effect dialog of the given class."""
        # Early out if there is no image.
        if not self.get_current_image():
            return

        # Check if there already is an effect dialog and eventually close it.
        if self._current_effect_dialog:
            result = QMessageBox.question(
                self.widget,
                "Are you sure?",
                "The current effect dialog will be closed and its effect will be lost. Do you want to continue?"
            )
            if result != QMessageBox.Yes:
                return
            self._current_effect_dialog.reject()

        # Create image backup that can be restored if the effect dialog is rejected.
        assert self._current_image_before_effect is None
        self._current_image_before_effect = self.get_current_image().copy()

        # Show the effect dialog.
        assert self._current_effect_dialog is None
        assert issubclass(cls, EffectDialog)
        self._current_effect_dialog = cls(self.widget)
        self._current_effect_dialog.update_image.connect(self.set_current_image)
        self._current_effect_dialog.accepted.connect(self._accept_current_effect)
        self._current_effect_dialog.rejected.connect(self._reject_current_effect)
        try:
            self._current_effect_dialog.set_input_pixmap(self.get_current_image())
        except Exception:
            _logger.exception("An exception occurred in set_input_pixmap() of effect dialog of type {}.".format(cls))
            QMessageBox.warning(self.widget, "Error", "An error occurred, see log for more info.")
            self._reject_current_effect()
            return
        self._image_widget.mouse_moved.connect(self._current_effect_dialog.pixel_hovered)
        self._image_widget.mouse_pressed.connect(self._current_effect_dialog.pixel_clicked)
        self._current_effect_dialog.show()

    def _accept_current_effect(self) -> None:
        """Deletes the current effect dialog and deletes the image backup from before the effect."""
        assert isinstance(self._current_effect_dialog, EffectDialog)
        self._current_effect_dialog.deleteLater()
        self._current_effect_dialog = None
        assert isinstance(self._current_image_before_effect, QPixmap)
        self._current_image_before_effect = None
        self.add_image_to_history(self.get_current_image())

    def _reject_current_effect(self) -> None:
        """Deletes the current effect dialog and restores the image backup from before the effect."""
        assert isinstance(self._current_effect_dialog, EffectDialog)
        self._current_effect_dialog.deleteLater()
        self._current_effect_dialog = None
        assert isinstance(self._current_image_before_effect, QPixmap)
        self.set_current_image(self._current_image_before_effect)
        self._current_image_before_effect = None

    def _get_widget(self) -> QMainWindow:
        assert isinstance(self.widget, QMainWindow)
        return self.widget

    def _get_layout_current_image(self) -> QLayout:
        assert isinstance(self.widget.layoutCurrentImage, QLayout)
        return self.widget.layoutCurrentImage

    def _get_action_open_file(self) -> QAction:
        assert isinstance(self.widget.actionOpenFile, QAction)
        return self.widget.actionOpenFile

    def _get_action_save_file(self) -> QAction:
        assert isinstance(self.widget.actionSave, QAction)
        return self.widget.actionSave

    def _get_action_quit(self) -> QAction:
        assert isinstance(self.widget.actionQuit, QAction)
        return self.widget.actionQuit

    def _get_action_undo(self) -> QAction:
        assert isinstance(self.widget.actionUndo, QAction)
        return self.widget.actionUndo

    def _get_action_redo(self) -> QAction:
        assert isinstance(self.widget.actionRedo, QAction)
        return self.widget.actionRedo

    def _get_group_box_effects(self) -> QGroupBox:
        assert isinstance(self.widget.groupBoxEffects, QGroupBox)
        return self.widget.groupBoxEffects

    def _get_layout_effects(self) -> QLayout:
        assert isinstance(self.widget.layoutEffects, QLayout)
        return self.widget.layoutEffects


def main(argv=None):
    # Parse arguments.
    if argv is None:
        argv = sys.argv
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", default=0, action="count")
    args = parser.parse_args(argv[1:])

    # Set log level.
    log_levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    logging.basicConfig(level=log_levels[args.verbose])

    # Create application.
    QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(argv)
    gallery = Gallery()
    gallery.add_effect_dialog("Smooth", SmoothEffectDialog)
    gallery.add_effect_dialog("Main colors", MainColorsEffectDialog)
    gallery.add_effect_dialog("Edges", EdgeEffectDialog)
    gallery.add_effect_dialog("Paint by number", PaintByNumberEffectDialog)
    gallery.widget.show()
    return app.exec_()


if __name__ == "__main__":
    main()
