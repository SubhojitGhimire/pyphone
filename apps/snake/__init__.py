from .snake import SnakeApp

def get_app_info():
    return {
        "name": "Snake",
        "icon": "apps/snake/icon.png",
        "widget": SnakeApp
    }