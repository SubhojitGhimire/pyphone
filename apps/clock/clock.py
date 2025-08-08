import pytz
import datetime
from PySide6.QtCore import QTimer, QTime, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QLabel, QPushButton, QHBoxLayout, QTimeEdit, QProgressBar, QScrollArea

class ClockApp(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Clock")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        tabs = QTabWidget()
        tabs.addTab(self.create_world_clock_tab(), "World Clock")
        tabs.addTab(self.create_stopwatch_tab(), "Stopwatch")
        tabs.addTab(self.create_timer_tab(), "Timer")
        
        main_layout.addWidget(tabs)

    def create_world_clock_tab(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.world_clocks = []
        timezones = ["Asia/Kathmandu", "America/New_York", "Europe/London"]

        for tz in timezones:
            tz_obj = pytz.timezone(tz)
            city = tz.split('/')[-1].replace('_', ' ')
            
            time_label = QLabel("00:00:00", font=self.font())
            time_label.setStyleSheet("font-size: 28px; font-weight: bold;")
            
            city_label = QLabel(city, font=self.font())
            city_label.setStyleSheet("font-size: 16px; color: #AAA;")
            
            layout.addWidget(time_label)
            layout.addWidget(city_label)
            layout.addSpacing(20)
            
            self.world_clocks.append({'label': time_label, 'tz': tz_obj})

        self.world_clock_timer = QTimer(self)
        self.world_clock_timer.timeout.connect(self.update_world_clocks)
        self.world_clock_timer.start(1000)
        return container

    def update_world_clocks(self):
        for clock in self.world_clocks:
            current_time = datetime.datetime.now(clock['tz'])
            clock['label'].setText(current_time.strftime("%H:%M:%S"))

    def create_stopwatch_tab(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.stopwatch_time = QTime(0, 0, 0, 0)
        self.stopwatch_label = QLabel("00:00:00.000")
        self.stopwatch_label.setStyleSheet("font-size: 40px; font-weight: bold;")
        
        self.stopwatch_timer = QTimer(self)
        self.stopwatch_timer.timeout.connect(self.update_stopwatch)
        
        self.lap_area = QScrollArea()
        self.lap_area.setWidgetResizable(True)
        self.lap_widget = QWidget()
        self.lap_layout = QVBoxLayout(self.lap_widget)
        self.lap_area.setWidget(self.lap_widget)

        btn_layout = QHBoxLayout()
        self.sw_start_btn = QPushButton("Start")
        self.sw_stop_btn = QPushButton("Stop")
        self.sw_reset_btn = QPushButton("Reset")
        self.sw_lap_btn = QPushButton("Lap")
        btn_layout.addWidget(self.sw_start_btn)
        btn_layout.addWidget(self.sw_stop_btn)
        btn_layout.addWidget(self.sw_reset_btn)
        btn_layout.addWidget(self.sw_lap_btn)

        self.sw_start_btn.clicked.connect(self.start_stopwatch)
        self.sw_stop_btn.clicked.connect(self.stop_stopwatch)
        self.sw_reset_btn.clicked.connect(self.reset_stopwatch)
        self.sw_lap_btn.clicked.connect(self.record_lap)

        layout.addWidget(self.stopwatch_label, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lap_area)
        layout.addLayout(btn_layout)
        return container

    def start_stopwatch(self): self.stopwatch_timer.start(1)
    def stop_stopwatch(self): self.stopwatch_timer.stop()
    def reset_stopwatch(self):
        self.stopwatch_timer.stop()
        self.stopwatch_time.setHMS(0, 0, 0, 0)
        self.stopwatch_label.setText("00:00:00.000")
        while self.lap_layout.count(): self.lap_layout.takeAt(0).widget().deleteLater()

    def update_stopwatch(self):
        self.stopwatch_time = self.stopwatch_time.addMSecs(1)
        self.stopwatch_label.setText(self.stopwatch_time.toString("mm:ss:zzz"))

    def record_lap(self):
        lap_time = self.stopwatch_label.text()
        lap_label = QLabel(lap_time)
        self.lap_layout.insertWidget(0, lap_label)

    def create_timer_tab(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm:ss")
        self.time_edit.setStyleSheet("font-size: 40px;")
        
        self.timer_progress = QProgressBar()
        
        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self.update_countdown)
        
        btn_layout = QHBoxLayout()
        self.timer_start_btn = QPushButton("Start")
        self.timer_pause_btn = QPushButton("Pause")
        self.timer_reset_btn = QPushButton("Reset")
        btn_layout.addWidget(self.timer_start_btn)
        btn_layout.addWidget(self.timer_pause_btn)
        btn_layout.addWidget(self.timer_reset_btn)

        self.timer_start_btn.clicked.connect(self.start_timer)
        self.timer_pause_btn.clicked.connect(self.pause_timer)
        self.timer_reset_btn.clicked.connect(self.reset_timer)

        layout.addWidget(self.time_edit)
        layout.addWidget(self.timer_progress)
        layout.addLayout(btn_layout)
        return container

    def start_timer(self):
        self.total_seconds = self.time_edit.time().hour() * 3600 + self.time_edit.time().minute() * 60 + self.time_edit.time().second()
        self.remaining_seconds = self.total_seconds
        if self.total_seconds > 0:
            self.timer_progress.setMaximum(self.total_seconds)
            self.timer_progress.setValue(self.total_seconds)
            self.countdown_timer.start(1000)

    def pause_timer(self): self.countdown_timer.stop()
    def reset_timer(self):
        self.countdown_timer.stop()
        self.time_edit.setTime(QTime(0, 0, 0))
        self.timer_progress.setValue(0)

    def update_countdown(self):
        self.remaining_seconds -= 1
        hours = self.remaining_seconds // 3600
        minutes = (self.remaining_seconds % 3600) // 60
        seconds = self.remaining_seconds % 60
        self.time_edit.setTime(QTime(hours, minutes, seconds))
        self.timer_progress.setValue(self.remaining_seconds)
        if self.remaining_seconds <= 0:
            self.countdown_timer.stop()