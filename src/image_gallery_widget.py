import os
from PyQt6.QtCore import Qt
from src.image_model import ImageModel
from PyQt6.QtWidgets import (
    QLabel,
    QWidget,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
)
from PyQt6.QtGui import QPixmap


class ImageGalleryWidget(QWidget):
    """
    The central widget displaying the current image,
    with Previous/Next buttons. Connects to an ImageModel
    to load images and update the display.
    """

    def __init__(self, model: ImageModel):
        super().__init__()
        self._model = model
        # Widgets
        self._image_label = QLabel("No image loaded.")
        self._image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._prev_button = QPushButton("Previous")
        self._next_button = QPushButton("Next")
        # Layouts
        button_layout = QHBoxLayout()
        button_layout.addWidget(self._prev_button)
        button_layout.addWidget(self._next_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self._image_label, stretch=1)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        # Button Signals
        self._prev_button.clicked.connect(self.show_previous_image)
        self._next_button.clicked.connect(self.show_next_image)

    def load_current_image(self):
        """
        Loads the current image from the model, if any.
        """
        path = self._model.get_current_image_path()
        if path and os.path.isfile(path):
            pixmap = QPixmap(path)

            # Optionally scale to label
            scale_pixmap = pixmap.scaled(
                self._image_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self._image_label.setPixmap(scale_pixmap)
        else:
            self._image_label.setText("No image loaded.")

    def show_previous_image(self):
        self._model.previous_image()
        self.load_current_image()

    def show_next_image(self):
        self._model.next_image()
        self.load_current_image()

    def resizeEvent(self, event):
        """
        Called when the widget is resized (so we can re-scale the image).
        """
        super().resizeEvent(event)
        self.load_current_image()
