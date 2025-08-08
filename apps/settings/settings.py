from PySide6.QtGui import QFontDatabase
from PySide6.QtCore import Signal, QSize
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QStackedWidget, QListWidget, QColorDialog, QFileDialog, QListWidgetItem

class SettingsApp(QWidget):
    settings_changed = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = {}

        main_layout = QHBoxLayout(self)
        
        self.nav_list = QListWidget()
        self.nav_list.setFixedWidth(100)
        main_layout.addWidget(self.nav_list)
        
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        self.create_appearance_page()
        self.create_clock_page()
        
        self.nav_list.currentRowChanged.connect(self.stack.setCurrentIndex)

    def set_initial_settings(self, settings):
        self.settings = settings
        self.theme_combo.setCurrentText(self.settings.get("theme", "Dark"))
        self.font_combo.setCurrentText(self.settings.get("font_family", "Roboto"))
        self.fontsize_combo.setCurrentText(self.settings.get("font_size", "Medium"))
        self.clockformat_combo.setCurrentText(self.settings.get("clock_format", "12-Hour"))

    def create_appearance_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        self.nav_list.addItem("Appearance")

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light"])
        self.theme_combo.currentTextChanged.connect(lambda v: self.emit_setting("theme", v))
        layout.addWidget(QLabel("Theme"))
        layout.addWidget(self.theme_combo)

        self.font_combo = QComboBox()
        self.font_combo.addItems(QFontDatabase.families())
        self.font_combo.currentTextChanged.connect(lambda v: self.emit_setting("font_family", v))
        layout.addWidget(QLabel("Font Family"))
        layout.addWidget(self.font_combo)

        self.fontsize_combo = QComboBox()
        self.fontsize_combo.addItems(["Small", "Medium", "Large"])
        self.fontsize_combo.currentTextChanged.connect(lambda v: self.emit_setting("font_size", v))
        layout.addWidget(QLabel("Font Size"))
        layout.addWidget(self.fontsize_combo)

        wallpaper_btn = QPushButton("Choose Wallpaper Image...")
        wallpaper_btn.clicked.connect(self.choose_wallpaper_image)
        color_btn = QPushButton("Choose Wallpaper Color...")
        color_btn.clicked.connect(self.choose_wallpaper_color)
        layout.addWidget(QLabel("Wallpaper"))
        layout.addWidget(wallpaper_btn)
        layout.addWidget(color_btn)
        
        layout.addStretch()
        self.stack.addWidget(page)

    def create_clock_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        self.nav_list.addItem("Clock")
        
        self.clockformat_combo = QComboBox()
        self.clockformat_combo.addItems(["12-Hour", "24-Hour"])
        self.clockformat_combo.currentTextChanged.connect(lambda v: self.emit_setting("clock_format", v))
        layout.addWidget(QLabel("Homescreen Clock Format"))
        layout.addWidget(self.clockformat_combo)
        
        layout.addStretch()
        self.stack.addWidget(page)

    def choose_wallpaper_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Wallpaper", "", "Images (*.png *.jpg)")
        if path:
            self.emit_setting("wallpaper", {"type": "image", "value": path})

    def choose_wallpaper_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.emit_setting("wallpaper", {"type": "color", "value": color.name()})

    def emit_setting(self, key, value):
        self.settings[key] = value
        self.settings_changed.emit(self.settings)