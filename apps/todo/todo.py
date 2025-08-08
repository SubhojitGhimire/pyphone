import os
import json
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QTextCharFormat, QColor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QCheckBox, QLabel, QTabWidget, QCalendarWidget, QInputDialog

class TaskItemWidget(QWidget):
    def __init__(self, text, is_completed=False):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(is_completed)
        self.label = QLabel(text)
        layout.addWidget(self.checkbox)
        layout.addWidget(self.label, 1)

class PlannerApp(QWidget):
    DAILY_TODO_FILE = "daily_todo_data.json"
    EVENT_PLANNER_FILE = "event_planner_data.json"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.event_data = {}

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        tabs = QTabWidget()
        
        tabs.addTab(self.create_daily_todo_tab(), "Daily List")
        tabs.addTab(self.create_event_planner_tab(), "Event Planner")

        main_layout.addWidget(tabs)
        self.setLayout(main_layout)

    def create_daily_todo_tab(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        
        input_layout = QHBoxLayout()
        self.daily_task_input = QLineEdit(placeholderText="Enter a daily task...")
        add_btn = QPushButton("Add")
        add_btn.clicked.connect(self.add_daily_task)
        input_layout.addWidget(self.daily_task_input)
        input_layout.addWidget(add_btn)

        self.daily_task_list = QListWidget()
        delete_btn = QPushButton("Delete Completed")
        delete_btn.clicked.connect(self.delete_daily_completed)
        
        layout.addLayout(input_layout)
        layout.addWidget(self.daily_task_list)
        layout.addWidget(delete_btn)
        
        self.load_daily_tasks()
        return container

    def load_daily_tasks(self):
        if not os.path.exists(self.DAILY_TODO_FILE): return
        try:
            with open(self.DAILY_TODO_FILE, 'r') as f: tasks = json.load(f)
            for task in tasks:
                self._add_task_to_daily_list(task['text'], task['completed'])
        except (json.JSONDecodeError, KeyError): pass

    def save_daily_tasks(self):
        tasks = []
        for i in range(self.daily_task_list.count()):
            item = self.daily_task_list.item(i)
            widget = self.daily_task_list.itemWidget(item)
            tasks.append({"text": widget.label.text(), "completed": widget.checkbox.isChecked()})
        with open(self.DAILY_TODO_FILE, 'w') as f: json.dump(tasks, f, indent=4)

    def add_daily_task(self):
        text = self.daily_task_input.text().strip()
        if text:
            self._add_task_to_daily_list(text)
            self.daily_task_input.clear()
            self.save_daily_tasks()

    def _add_task_to_daily_list(self, text, completed=False):
        widget = TaskItemWidget(text, completed)
        widget.checkbox.stateChanged.connect(self.save_daily_tasks)
        item = QListWidgetItem(self.daily_task_list)
        item.setSizeHint(widget.sizeHint())
        self.daily_task_list.addItem(item)
        self.daily_task_list.setItemWidget(item, widget)

    def delete_daily_completed(self):
        for i in range(self.daily_task_list.count() - 1, -1, -1):
            item = self.daily_task_list.item(i)
            if self.daily_task_list.itemWidget(item).checkbox.isChecked():
                self.daily_task_list.takeItem(i)
        self.save_daily_tasks()

    def create_event_planner_tab(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        
        self.calendar = QCalendarWidget()
        self.calendar.selectionChanged.connect(self.update_event_list)
        
        self.event_list = QListWidget()
        
        add_event_btn = QPushButton("Add Event to Selected Date")
        add_event_btn.clicked.connect(self.add_event)
        
        layout.addWidget(self.calendar)
        layout.addWidget(QLabel("Events for selected date:"))
        layout.addWidget(self.event_list)
        layout.addWidget(add_event_btn)
        
        self.load_events()
        return container

    def load_events(self):
        if os.path.exists(self.EVENT_PLANNER_FILE):
            try:
                with open(self.EVENT_PLANNER_FILE, 'r') as f: self.event_data = json.load(f)
            except json.JSONDecodeError: self.event_data = {}
        self.mark_event_dates()
        self.update_event_list()

    def save_events(self):
        date_key = self.calendar.selectedDate().toString("yyyy-MM-dd")
        if date_key in self.event_data:
            current_events = []
            for i in range(self.event_list.count()):
                item = self.event_list.item(i)
                widget = self.event_list.itemWidget(item)
                current_events.append({"text": widget.label.text(), "completed": widget.checkbox.isChecked()})
            self.event_data[date_key] = current_events
        
        with open(self.EVENT_PLANNER_FILE, 'w') as f: json.dump(self.event_data, f, indent=4)
        self.mark_event_dates()

    def update_event_list(self):
        self.event_list.clear()
        date_key = self.calendar.selectedDate().toString("yyyy-MM-dd")
        for event in self.event_data.get(date_key, []):
            widget = TaskItemWidget(event['text'], event['completed'])
            widget.checkbox.stateChanged.connect(self.save_events)
            item = QListWidgetItem(self.event_list)
            item.setSizeHint(widget.sizeHint())
            self.event_list.addItem(item)
            self.event_list.setItemWidget(item, widget)

    def add_event(self):
        date = self.calendar.selectedDate()
        text, ok = QInputDialog.getText(self, "Add Event", f"Enter event for {date.toString('MMMM d, yyyy')}:")
        if ok and text:
            date_key = date.toString("yyyy-MM-dd")
            if date_key not in self.event_data:
                self.event_data[date_key] = []
            self.event_data[date_key].append({"text": text, "completed": False})
            self.save_events()
            self.update_event_list()

    def mark_event_dates(self):
        fmt = QTextCharFormat()
        fmt.setForeground(QColor("lightblue"))
        fmt.setFontWeight(700)
        for date_str, events in self.event_data.items():
            if events:
                self.calendar.setDateTextFormat(QDate.fromString(date_str, "yyyy-MM-dd"), fmt)