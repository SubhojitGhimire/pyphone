# core/main_window.py

import os
import json
import importlib
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QStackedWidget

from core.status_bar import StatusBar
from core.app_drawer import AppDrawer
from core.homescreen import HomeScreen
from core.navigation_bar import NavigationBar

from apps.settings.settings import SettingsApp

class MainWindow(QMainWindow):
    SETTINGS_FILE = "settings.json"

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyPhone")
        self.setFixedSize(380, 800)

        self.screen_history = [0]
        self.app_widgets = {}
        self.current_settings = self.load_settings()

        self.available_apps = self.discover_apps()
        phone_body = QWidget()
        phone_body.setObjectName("PhoneBody")
        self.main_layout = QVBoxLayout(phone_body)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0,0,0,0)
        
        self.status_bar = StatusBar()
        self.screen_area = QStackedWidget()
        self.navigation_bar = NavigationBar()
        
        self.main_layout.addWidget(self.status_bar)
        self.main_layout.addWidget(self.screen_area, 1)
        self.main_layout.addWidget(self.navigation_bar)
        self.setCentralWidget(phone_body)

        self.setup_core_screens()
        self.connect_signals()

    def load_settings(self):
        if os.path.exists(self.SETTINGS_FILE):
            with open(self.SETTINGS_FILE, 'r') as f:
                return json.load(f)
        return {"theme": "Dark", "wallpaper": ":/assets/wallpapers/default.png"}

    def save_settings(self):
        with open(self.SETTINGS_FILE, 'w') as f:
            json.dump(self.current_settings, f, indent=4)

    def on_theme_changed(self, theme_name):
        self.current_settings['theme'] = theme_name
        self.apply_theme()
        self.save_settings()

    def on_wallpaper_changed(self, path):
        self.current_settings['wallpaper'] = path
        self.homescreen.set_new_wallpaper(path)
        self.save_settings()

    def apply_theme(self):
        style_sheet = "styles/main_style.qss" if self.current_settings['theme'] == "Dark" else "styles/light_style.qss"
        try:
            with open(style_sheet, 'r') as f:
                self.parent().setStyleSheet(f.read())
        except FileNotFoundError: pass

    def discover_apps(self):
        apps_info = {}
        apps_dir = "apps"
        for app_name in os.listdir(apps_dir):
            app_path = os.path.join(apps_dir, app_name)
            if os.path.isdir(app_path) and "__init__.py" in os.listdir(app_path):
                try:
                    module = importlib.import_module(f"apps.{app_name}")
                    if hasattr(module, "get_app_info"):
                        apps_info[app_name] = module.get_app_info()
                except Exception as e: pass
        return apps_info

    def setup_core_screens(self):
        self.homescreen = HomeScreen()
        self.homescreen.set_new_wallpaper(self.current_settings['wallpaper'])
        self.screen_area.addWidget(self.homescreen)

        self.app_drawer = AppDrawer(self.available_apps)
        self.screen_area.addWidget(self.app_drawer)

    def connect_signals(self):
        self.navigation_bar.home_button.clicked.connect(self.go_to_home)
        self.navigation_bar.apps_button.clicked.connect(self.go_to_app_drawer)
        self.navigation_bar.back_button.clicked.connect(self.go_back)
        self.app_drawer.app_launched.connect(self.launch_app)
        self.homescreen.dock_app_launched.connect(self.launch_app)

    def launch_app(self, app_widget_class):
        app_name = app_widget_class.__name__
        if app_name not in self.app_widgets:
            app_instance = app_widget_class()
            
            if isinstance(app_instance, SettingsApp):
                app_instance.theme_changed.connect(self.on_theme_changed)
                app_instance.wallpaper_changed.connect(self.on_wallpaper_changed)
                app_instance.set_initial_theme(self.current_settings['theme'])

            app_container = QWidget()
            layout = QGridLayout(app_container)
            layout.addWidget(app_instance, 1, 1)
            layout.setRowStretch(0, 1); layout.setRowStretch(2, 1)
            layout.setColumnStretch(0, 1); layout.setColumnStretch(2, 1)
            new_index = self.screen_area.addWidget(app_container)
            self.app_widgets[app_name] = new_index
        
        target_index = self.app_widgets[app_name]
        self.navigate_to(target_index)

    def navigate_to(self, index):
        if index != self.screen_area.currentIndex():
            self.screen_area.setCurrentIndex(index)
            if not self.screen_history or self.screen_history[-1] != index:
                 self.screen_history.append(index)

    def go_to_home(self): self.navigate_to(0)
    def go_to_app_drawer(self): self.navigate_to(1)
        
    def go_back(self):
        if len(self.screen_history) > 1:
            self.screen_history.pop()
            prev_index = self.screen_history[-1]
            self.screen_area.setCurrentIndex(prev_index)
        else:
            self.screen_history = [0]
            self.screen_area.setCurrentIndex(0)