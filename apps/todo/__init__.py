from .todo import PlannerApp

def get_app_info():
    return {
        "name": "Planner",
        "icon": "apps/todo/icon.png",
        "widget": PlannerApp
    }