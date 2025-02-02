from src.thumbnails_list_widget import ThumbnailListWidget


class ImageModel:
    """
    Holds the list of image paths, and the current index.
    Manages navigation logic for next/previous images.
    """

    def __init__(self):
        self._image_paths = []
        self._current_index = -1
        self._thumbnails_list = None

    def set_images(
        self,
        image_paths: list[str],
        thumbnails_list: ThumbnailListWidget,
    ):
        self._image_paths = image_paths
        self._current_index = 0 if image_paths else -1
        self._thumbnails_list = thumbnails_list

    def get_current_image_path(self):
        if 0 <= self._current_index < len(self._image_paths):
            return self._image_paths[self._current_index]
        return None

    def next_image(self):
        if 0 <= self._current_index < len(self._image_paths) - 1:
            self._current_index += 1
            if self._thumbnails_list:
                self._thumbnails_list.select_index(self._current_index)

    def previous_image(self):
        """
        Move to the previous image, if possible.
        """
        if self._current_index > 0:
            self._current_index -= 1
            if self._thumbnails_list:
                self._thumbnails_list.select_index(self._current_index)

    def jump_to_index(self, index):
        if 0 <= index < len(self._image_paths):
            self._current_index = index
            if self._thumbnails_list:
                self._thumbnails_list.select_index(self._current_index)
