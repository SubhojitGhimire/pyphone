import psutil
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QTimer, QTime, Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel

class StatusBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(35)
        self.setStyleSheet("color: white; font-size: 14px;")

        layout = QHBoxLayout()
        layout.setContentsMargins(15, 0, 15, 0)

        self.time_label = QLabel()
        
        self.wifi_icon = QLabel()
        self.wifi_icon.setPixmap(QPixmap(":/assets/icons/wifi.png").scaledToHeight(16, Qt.TransformationMode.SmoothTransformation))
        
        self.battery_label = QLabel()
        
        layout.addWidget(self.time_label)
        layout.addStretch()
        layout.addWidget(self.wifi_icon)
        layout.addWidget(self.battery_label)
        
        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status)
        self.timer.start(1000)
        self.update_status()

    def update_status(self):
        self.time_label.setText(QTime.currentTime().toString("h:mm"))
        
        battery = psutil.sensors_battery()
        if battery:
            percent = int(battery.percent)
            self.battery_label.setText(f"{percent}%")
        else:
            self.battery_label.setText("100%")