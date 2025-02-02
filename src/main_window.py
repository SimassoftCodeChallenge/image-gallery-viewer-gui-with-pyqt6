import os
from PyQt6.QtWidgets import (
    QMenu,
    QWidget,
    QMenuBar,
    QMainWindow,
    QHBoxLayout,
    QFileDialog,
    QMessageBox,
)

from PyQt6.QtCore import QTimer, Qt
from src.image_model import ImageModel
from PyQt6.QtGui import QKeySequence, QAction
from src.image_gallery_widget import ImageGalleryWidget
from src.thumbnails_list_widget import ThumbnailListWidget


class MainWindow(QMainWindow):
    """
    Combines the ImageGalleryWidget (center),
    the ThumbnailsListWidget (left), and a member for
    opening folders and starting/stopping a slideshow
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Customizable Image Gallery")
        self.resize(1200, 800)

        # Model
        self._model: ImageModel = ImageModel()        

        # Widgets
        self._image_gallery_widget = ImageGalleryWidget(self._model)
        self._thumbnails_list = ThumbnailListWidget(self.on_thumbnails_selected)
        self._model.set_images([], self._thumbnails_list)
        # Timer for Slideshow
        self._slideshow_timer = QTimer()
        self._slideshow_timer.setInterval(2000)  # 2 seconds per image
        self._slideshow_timer.timeout.connect(self.handle_slideshow_step)
        self._slideshow_running = True

        # Layout
        central_widget = QWidget()
        main_layout = QHBoxLayout()
        main_layout.addWidget(self._thumbnails_list, stretch=1)
        main_layout.addWidget(self._image_gallery_widget, stretch=3)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Menubar
        menubar = self.menuBar() if self.menuBar() else QMenuBar(self)
        file_menu = menubar.addMenu("File")
        slideshow_menu = menubar.addMenu("Slideshow")

        open_folder_action = QAction("Open Folder", self)
        open_folder_action.triggered.connect(self.open_folder)
        file_menu.addAction(open_folder_action)

        start_slideshow_action = QAction("Start Slideshow", self)
        start_slideshow_action.triggered.connect(self.start_slideshow)
        slideshow_menu.addAction(start_slideshow_action)

        stop_slideshow_action = QAction("Stop Slideshow", self)
        stop_slideshow_action.triggered.connect(self.stop_slideshow)
        slideshow_menu.addAction(stop_slideshow_action)

        # Keyboard shortcut (Left/Right arrow keys)
        prev_action = QAction("Previous", self)
        prev_action.setShortcut(QKeySequence(Qt.Key.Key_Left))
        prev_action.triggered.connect(self.show_previous_image)
        self.addAction(prev_action)

        next_action = QAction("Next", self)
        next_action.setShortcut(QKeySequence(Qt.Key.Key_Right))
        next_action.triggered.connect(self.show_next_image)
        self.addAction(next_action)

    def open_folder(self):
        """
        Opens a folder dialog and loads images into the model
        """
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "Select Folder",
        )
        if folder_path:
            valid_extensions = {
                ".png",
                ".jpg",
                ".jpeg",
                ".bmp",
                ".gif",
            }
            image_paths = [
                os.path.join(folder_path, f)
                for f in os.listdir(folder_path)
                if os.path.splitext(f.lower())[1] in valid_extensions
            ]
            image_paths.sort()

            if not image_paths:
                QMessageBox.warning(self, "Warning", "No images found in this folder")
                return

            self._model.set_images(image_paths, self._thumbnails_list)

            # Update UI
            self._image_gallery_widget.load_current_image()
            self._thumbnails_list.populate(image_paths)
            self._thumbnails_list.select_index(self._model._current_index)

    def start_slideshow(self):
        if self._model._image_paths:
            self._slideshow_timer.start()
            self._slideshow_running = True

    def stop_slideshow(self):
        self._slideshow_timer.stop()
        self._slideshow_running = False

    def handle_slideshow_step(self):
        """
        Move to the next image automatically. If we reach the end, wrap around.
        """

        if not self._model._image_paths:
            return

        if self._model._current_index >= len(self._model._image_paths) - 1:
            # Wrap to First
            self._model._current_index = 0
        else:
            self._model.next_image()

        self.update_display()

    def on_thumbnails_selected(self, index):
        """
        Called when user selects a thumbnail in the list.
        """
        self._model.jump_to_index(index)
        self.update_display()

    def show_previous_image(self):
        self._model.previous_image()
        self.update_display()

    def show_next_image(self):
        self._model.next_image()
        self.update_display()

    def update_display(self):
        self._image_gallery_widget.load_current_image()
        self._thumbnails_list.select_index(self._model._current_index)
