from .browser import BrowserApp

def get_app_info():
    return {
        "name": "Browser",
        "icon": "apps/browser/icon.png",
        "widget": BrowserApp
    }