from PySide6.QtGui import QIcon
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QVBoxLayout, QLabel

class AppDrawer(QWidget):
    app_launched = Signal(type) 

    def __init__(self, apps_info: dict, parent=None):
        super().__init__(parent)
        self.setObjectName("AppDrawer")
        self.setStyleSheet("background-color: #2e2e2e;")

        self.main_layout = QGridLayout()
        self.main_layout.setSpacing(15)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        
        self.populate_apps(apps_info)
        
        self.main_layout.setRowStretch(self.main_layout.rowCount(), 1)
        self.main_layout.setColumnStretch(self.main_layout.columnCount(), 1)
        
        self.setLayout(self.main_layout)

    def populate_apps(self, apps_info: dict):
        col_count = 4
        row, col = 0, 0
        for app_key, info in apps_info.items():
            self.create_app_icon(info, row, col)
            col += 1
            if col >= col_count:
                col = 0
                row += 1
    
    def create_app_icon(self, info, row, col):
        """Creates a clickable icon for an app."""
        app_widget_class = info["widget"]

        icon_button = QPushButton()
        icon_button.setIcon(QIcon(info["icon"]))
        icon_button.setIconSize(icon_button.sizeHint().__mul__(3))
        icon_button.setFixedSize(64, 64)
        icon_button.setStyleSheet("background-color: transparent; border: none;")
        icon_button.clicked.connect(lambda: self.app_launched.emit(app_widget_class))

        name_label = QLabel(info["name"])
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setStyleSheet("color: white; font-size: 12px;")
        
        vbox = QVBoxLayout()
        vbox.addWidget(icon_button)
        vbox.addWidget(name_label)
        vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addLayout(vbox, row, col)