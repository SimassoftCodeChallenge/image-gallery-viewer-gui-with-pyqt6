import os
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QListWidget, QListWidgetItem


class ThumbnailListWidget(QListWidget):
    """
    Displays a list of image filenames (or actual thumbnails) on the side.
    When an item is selected, it calls a callback to let the main app
    switch to that image
    """

    def __init__(self, on_item_selected=None):
        super().__init__()
        self._on_item_selected = on_item_selected
        self.setIconSize(QSize(60, 60))  # Adjust thumbnail icon size as needed

        # Connect the selection signal
        self.itemSelectionChanged.connect(self.handle_selection_changed)

    def populate(self, image_paths):
        """
        Clears the list and re-populates with given image paths.
        Here, we add items with either icons or text.
        """
        self.clear()
        for path in image_paths:
            item = QListWidgetItem(os.path.basename(path))
            # If you wanna to show a small thumbnail icon:
            # pixmap = QPixmax(path)
            # icon = QIcon(
            # pixmap.scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio)
            # )
            # item.setIcon(icon)
            self.addItem(item)

    def handle_selection_changed(self):
        # Use currentIndex() to get the selected item
        selected_item = self.currentIndex()
        if selected_item.isValid():  # Check if the item is selected
            selected_index = selected_item.row()  # Get the index of the selected item
            if self._on_item_selected:
                self._on_item_selected(selected_index)

    def select_index(self, index):
        """
        Programmatically select an index in the list.
        """
        if 0 <= index < self.count():
            self.setCurrentRow(index)
