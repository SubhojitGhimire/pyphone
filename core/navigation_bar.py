from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton

class NavigationBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(50)
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
            }
        """)

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 0, 10, 0)

        self.back_button = QPushButton()
        self.back_button.setIcon(QIcon(":/assets/icons/back.png"))
        self.back_button.setIconSize(QSize(24, 24))

        self.home_button = QPushButton()
        self.home_button.setIcon(QIcon(":/assets/icons/home.png"))
        self.home_button.setIconSize(QSize(28, 28))

        self.apps_button = QPushButton()
        self.apps_button.setIcon(QIcon(":/assets/icons/apps.png"))
        self.apps_button.setIconSize(QSize(24, 24))

        layout.addWidget(self.back_button)
        layout.addWidget(self.home_button)
        layout.addWidget(self.apps_button)

        self.setLayout(layout)