from .calculator import CalculatorApp

def get_app_info():
    return {
        "name": "Calculator",
        "icon": "apps/calculator/icon.png",
        "widget": CalculatorApp
    }