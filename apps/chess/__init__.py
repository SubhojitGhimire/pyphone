from .chess import ChessApp

def get_app_info():
    return { 
        "name": "Chess", 
        "icon": "apps/chess/icon.png", 
        "widget": ChessApp 
    }