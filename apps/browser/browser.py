from PySide6.QtCore import Qt
from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QProgressBar

class BrowserApp(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Browser")

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        controls = QWidget()
        controls_layout = QHBoxLayout(controls)
        controls_layout.setContentsMargins(5, 5, 5, 5)

        self.back_btn = QPushButton("<")
        self.fwd_btn = QPushButton(">")
        self.reload_btn = QPushButton("⟳")
        self.url_bar = QLineEdit()

        controls_layout.addWidget(self.back_btn)
        controls_layout.addWidget(self.fwd_btn)
        controls_layout.addWidget(self.reload_btn)
        controls_layout.addWidget(self.url_bar)

        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(3)
        self.progress_bar.setStyleSheet("QProgressBar { border: none; }")

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))

        main_layout.addWidget(controls)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.browser)

        self.back_btn.clicked.connect(self.browser.back)
        self.fwd_btn.clicked.connect(self.browser.forward)
        self.reload_btn.clicked.connect(self.browser.reload)
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        
        self.browser.urlChanged.connect(self.update_url_bar)
        self.browser.loadStarted.connect(lambda: self.progress_bar.setVisible(True))
        self.browser.loadProgress.connect(self.progress_bar.setValue)
        self.browser.loadFinished.connect(lambda: self.progress_bar.setVisible(False))

    def navigate_to_url(self):
        url_text = self.url_bar.text()
        if not (url_text.startswith("http://") or url_text.startswith("https://")):
            url_text = "https://" + url_text
        
        self.browser.setUrl(QUrl(url_text))

    def update_url_bar(self, q_url):
        self.url_bar.setText(q_url.toString())
        self.url_bar.setCursorPosition(0)