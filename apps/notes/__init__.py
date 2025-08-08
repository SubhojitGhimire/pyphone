from .notes import NotesApp

def get_app_info():
    return {
        "name": "Notes",
        "icon": "apps/notes/icon.png",
        "widget": NotesApp
    }