import os
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QLabel, QPushButton, QScrollArea, QGridLayout

class GalleryApp(QWidget):
    PHOTO_DIR = "assets/gallery_photos"
    THUMBNAIL_SIZE = 100

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gallery")

        self.stack = QStackedWidget(self)
        
        self.grid_view = self.create_grid_view()
        self.image_view = self.create_image_view()

        self.stack.addWidget(self.grid_view)
        self.stack.addWidget(self.image_view)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.addWidget(self.stack)

    def create_grid_view(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background-color: #1c1c1c; border: none;")

        container = QWidget()
        layout = QGridLayout(container)
        layout.setSpacing(5)

        image_files = [f for f in os.listdir(self.PHOTO_DIR) if f.endswith(('.png', '.jpg', '.jpeg'))]
        # Note: For a real-world app with many images, loading thumbnails should be done in a background thread to avoid freezing the UI.

        cols = 3
        for i, filename in enumerate(image_files):
            row, col = divmod(i, cols)
            
            thumb_button = QPushButton()
            thumb_button.setFixedSize(self.THUMBNAIL_SIZE, self.THUMBNAIL_SIZE)
            
            pixmap = QPixmap(os.path.join(self.PHOTO_DIR, filename))
            icon = QIcon(pixmap.scaled(self.THUMBNAIL_SIZE, self.THUMBNAIL_SIZE, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation))
            thumb_button.setIcon(icon)
            thumb_button.setIconSize(QSize(self.THUMBNAIL_SIZE, self.THUMBNAIL_SIZE))
            
            full_path = os.path.join(self.PHOTO_DIR, filename)
            thumb_button.clicked.connect(lambda path=full_path: self.show_image(path))
            
            layout.addWidget(thumb_button, row, col)

        scroll_area.setWidget(container)
        return scroll_area

    def create_image_view(self):
        container = QWidget()
        container.setStyleSheet("background-color: black;")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(5, 5, 5, 5)

        back_button = QPushButton("Back to Gallery")
        back_button.clicked.connect(self.show_grid)
        
        self.full_image_label = QLabel()
        self.full_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(back_button)
        layout.addWidget(self.full_image_label, 1) # '1' to stretch
        return container

    def show_image(self, image_path):
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaledToWidth(self.full_image_label.width(), Qt.TransformationMode.SmoothTransformation)
        self.full_image_label.setPixmap(scaled_pixmap)
        self.stack.setCurrentWidget(self.image_view)
        
    def show_grid(self):
        self.stack.setCurrentWidget(self.grid_view)