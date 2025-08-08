from PySide6.QtWidgets import QWidget, QGridLayout, QLineEdit, QPushButton
from PySide6.QtCore import Qt

class CalculatorApp(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Calculator")

        layout = QGridLayout()
        layout.setSpacing(5)

        self.display = QLineEdit()
        self.display.setPlaceholderText("0")
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setStyleSheet("font-size: 40px; min-height: 60px; border: 1px solid #555;")
        layout.addWidget(self.display, 0, 0, 1, 4)

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('C', 5, 0, 1, 4)
        ]

        for text, row, col, *span in buttons:
            button = QPushButton(text)
            button.setStyleSheet("font-size: 24px; min-height: 50px;")
            button.clicked.connect(self.on_button_clicked)
            if span:
                layout.addWidget(button, row, col, span[0], span[1])
            else:
                layout.addWidget(button, row, col)
        
        self.setLayout(layout)

    def on_button_clicked(self):
        button = self.sender()
        text = button.text()

        if text == '=':
            try:
                result = str(eval(self.display.text()))
                self.display.setText(result)
            except Exception:
                self.display.setText("Error")
        elif text == 'C':
            self.display.clear()
        else:
            self.display.setText(self.display.text() + text)