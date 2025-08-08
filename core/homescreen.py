import os
import importlib
from PySide6.QtGui import QIcon
from PySide6.QtCore import QTimer, QDateTime, Qt, Signal, QSize
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton


class HomeScreen(QWidget):
    dock_app_launched = Signal(type)

    def __init__(self, parent=None):

        super().__init__(parent)
        self.setObjectName("HomeScreen")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 20, 0, 0)
        main_layout.setSpacing(0)

        clock_widget = self.create_clock_widget()
        main_layout.addWidget(clock_widget, 0, Qt.AlignmentFlag.AlignTop)

        main_layout.addStretch()

        dock_widget = self.create_dock_widget()
        main_layout.addWidget(dock_widget, 0, Qt.AlignmentFlag.AlignBottom)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_datetime)
        self.timer.start(1000)
        self.update_datetime()

    def create_clock_widget(self):
        widget = QWidget()
        widget.setObjectName("HomeClockWidget")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(0)
        self.time_label = QLabel()
        self.time_label.setObjectName("HomeClockTime")
        self.date_label = QLabel()
        self.date_label.setObjectName("HomeClockDate")
        layout.addWidget(self.time_label)
        layout.addWidget(self.date_label)
        return widget

    def create_dock_widget(self):
        widget = QWidget()
        widget.setObjectName("HomeDock")
        widget.setFixedHeight(90)
        layout = QHBoxLayout(widget)

        dock_apps = ["gallery.png", "browser.png", "calculator.png"]
        for icon_file in dock_apps:
            try:
                btn = QPushButton()
                btn.setIcon(QIcon(f":/assets/icons/{icon_file}"))
                btn.setIconSize(QSize(50, 50))
                btn.setStyleSheet("background-color: transparent; border: none;")
                app_key = os.path.splitext(icon_file)[0]
                apps_dir = "apps"
                if app_key in os.listdir(apps_dir):
                    app_path = os.path.join(apps_dir, app_key)
                    if os.path.isdir(app_path) and "__init__.py" in os.listdir(app_path):
                        try:
                            mdl = importlib.import_module(f"apps.{app_key}")
                            if hasattr(mdl, "get_app_info"):
                                btn.clicked.connect(lambda: self.dock_app_launched.emit(mdl.get_app_info()["widget"]))
                        except Exception as e: pass
                layout.addWidget(btn)
            except Exception as e: continue
        
        return widget

    def update_datetime(self):
        now = QDateTime.currentDateTime()
        self.time_label.setText(now.toString("h:mm"))
        self.date_label.setText(now.toString("dddd, MMMM d"))

    def set_new_wallpaper(self, image_path):
        clean_path = image_path.replace("\\", "/")
        self.setStyleSheet(f"#HomeScreen {{ border-image: url({clean_path}) 0 0 0 0 stretch stretch; }}")
