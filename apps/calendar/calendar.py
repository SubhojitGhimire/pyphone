from PySide6.QtWidgets import QWidget, QVBoxLayout, QCalendarWidget

class CalendarApp(QWidget):
    """A simple, styled calendar app."""
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        calendar = QCalendarWidget()
        calendar.setObjectName("StyledCalendar")

        layout.addWidget(calendar)