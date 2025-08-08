from .clock import ClockApp

def get_app_info():
    return {
        "name": "Clock",
        "icon": "apps/clock/icon.png",
        "widget": ClockApp
    }