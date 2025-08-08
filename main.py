import sys
import resources_rc
from PySide6.QtGui import QFontDatabase
from core.main_window import MainWindow
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)

    QFontDatabase.addApplicationFont("assets/fonts/Roboto-Regular.ttf")
    QFontDatabase.addApplicationFont("assets/fonts/Roboto-Medium.ttf")

    try:
        with open("styles/main_style.qss", "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("Stylesheet not found.")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())