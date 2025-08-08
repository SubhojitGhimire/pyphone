from .weather import WeatherApp

def get_app_info():
    return {
        "name": "Weather",
        "icon": "apps/weather/icon.png",
        "widget": WeatherApp
    }