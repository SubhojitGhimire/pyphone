from .calendar import CalendarApp

def get_app_info():
    return {
        "name": "Calendar",
        "icon": "apps/calendar/icon.png",
        "widget": CalendarApp
    }