import os
import json
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QListWidget, QTextEdit, QPushButton, QVBoxLayout, QSplitter, QListWidgetItem

class NotesApp(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Notes")
        self.notes_file = "notes_data.json"
        self.notes = {}
        self._current_note_key = None
        self._block_signals = False

        main_layout = QHBoxLayout()
        splitter = QSplitter(Qt.Orientation.Horizontal)

        left_panel = QWidget()
        left_layout = QVBoxLayout()
        self.note_list = QListWidget()
        self.new_note_button = QPushButton("New Note")
        self.delete_note_button = QPushButton("Delete Note")
        left_layout.addWidget(self.new_note_button)
        left_layout.addWidget(self.delete_note_button)
        left_layout.addWidget(self.note_list)
        left_panel.setLayout(left_layout)

        self.text_editor = QTextEdit()
        self.text_editor.setPlaceholderText("Select a note or create a new one.")

        splitter.addWidget(left_panel)
        splitter.addWidget(self.text_editor)
        splitter.setSizes([150, 400])

        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

        self.load_notes()
        self.connect_signals()

    def connect_signals(self):
        self.new_note_button.clicked.connect(self.new_note)
        self.delete_note_button.clicked.connect(self.delete_note)
        self.note_list.currentItemChanged.connect(self.display_note)
        self.text_editor.textChanged.connect(self.save_current_note)

    def load_notes(self):
        if os.path.exists(self.notes_file):
            with open(self.notes_file, 'r') as f:
                self.notes = json.load(f)
        
        self.note_list.clear()
        for title in self.notes.keys():
            self.note_list.addItem(QListWidgetItem(title))

    def save_notes(self):
        with open(self.notes_file, 'w') as f:
            json.dump(self.notes, f, indent=4)

    def new_note(self):
        base_title = "New Note"
        title = base_title
        i = 1
        while title in self.notes:
            title = f"{base_title} {i}"
            i += 1
        
        self.notes[title] = ""
        item = QListWidgetItem(title)
        self.note_list.addItem(item)
        self.note_list.setCurrentItem(item)
        self.text_editor.setFocus()
        self.save_notes()

    def delete_note(self):
        current_item = self.note_list.currentItem()
        if not current_item:
            return

        title = current_item.text()
        if title in self.notes:
            del self.notes[title]
            self.note_list.takeItem(self.note_list.row(current_item))
            self.text_editor.clear()
            self.save_notes()

    def display_note(self, current_item, previous_item):
        if not current_item:
            self._current_note_key = None
            self.text_editor.clear()
            self.text_editor.setPlaceholderText("Select a note or create a new one.")
            return

        self._block_signals = True
        title = current_item.text()
        self._current_note_key = title
        self.text_editor.setText(self.notes.get(title, ""))
        self._block_signals = False

    def save_current_note(self):
        if self._block_signals or self._current_note_key is None:
            return

        current_text = self.text_editor.toPlainText()
        self.notes[self._current_note_key] = current_text
        self.save_notes()