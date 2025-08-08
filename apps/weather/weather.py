import requests
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QGridLayout, QFrame

class WeatherApp(QWidget):
    API_KEY = "ab67fbcae98263596786b707267909c1"
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Weather")
        
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        
        search_layout = QHBoxLayout()
        self.city_input = QLineEdit(placeholderText="Enter city name...")
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.fetch_weather)
        search_layout.addWidget(self.city_input)
        search_layout.addWidget(search_btn)
        main_layout.addLayout(search_layout)

        self.city_label = QLabel("Lalitpur")
        self.city_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        
        self.weather_icon = QLabel()
        
        self.temp_label = QLabel("--°C")
        self.temp_label.setStyleSheet("font-size: 72px; font-weight: 300;")
        
        self.description_label = QLabel("Weather conditions")
        self.description_label.setStyleSheet("font-size: 16px; color: #AAA;")
        
        main_layout.addWidget(self.city_label, 0, Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.weather_icon, 0, Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.temp_label, 0, Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.description_label, 0, Qt.AlignmentFlag.AlignCenter)

        details_frame = QFrame()
        details_frame.setFrameShape(QFrame.Shape.StyledPanel)
        details_grid = QGridLayout(details_frame)
        self.humidity_label = self.create_detail_label(details_grid, 0, "Humidity")
        self.wind_label = self.create_detail_label(details_grid, 1, "Wind Speed")
        self.precipitation_label = self.create_detail_label(details_grid, 2, "Precipitation (1h)")
        self.aqi_label = self.create_detail_label(details_grid, 3, "Air Quality")
        main_layout.addWidget(details_frame)
        
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red;")
        main_layout.addWidget(self.error_label)
        
        main_layout.addStretch()
        
        self.fetch_weather(city="Kathmandu")

    def create_detail_label(self, grid, row, name):
        grid.addWidget(QLabel(f"{name}:"), row, 0)
        value_label = QLabel("--")
        grid.addWidget(value_label, row, 1)
        return value_label

    def fetch_weather(self, city=None):
        if not city:
            city = self.city_input.text()
        if not city:
            return

        self.error_label.setText("")
        
        try:
            weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.API_KEY}&units=metric"
            response = requests.get(weather_url)
            weather_data = response.json()

            if response.status_code != 200:
                self.error_label.setText(f"Error: {weather_data.get('message', 'City not found')}")
                return

            lat, lon = weather_data['coord']['lat'], weather_data['coord']['lon']
            aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={self.API_KEY}"
            aqi_response = requests.get(aqi_url)
            aqi_data = aqi_response.json()
            
            self.update_ui(weather_data, aqi_data)

        except requests.exceptions.RequestException as e:
            self.error_label.setText(f"Error: Network connection failed.")

    def update_ui(self, weather, aqi):
        self.city_label.setText(weather['name'])
        self.temp_label.setText(f"{round(weather['main']['temp'])}°C")
        self.description_label.setText(weather['weather'][0]['description'].title())
        
        self.humidity_label.setText(f"{weather['main']['humidity']}%")
        self.wind_label.setText(f"{weather['wind']['speed']} m/s")
        self.precipitation_label.setText(f"{weather.get('rain', {}).get('1h', 0)} mm")

        aqi_index = aqi['list'][0]['main']['aqi']
        aqi_map = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}
        self.aqi_label.setText(aqi_map.get(aqi_index, "Unknown"))

        icon_code = weather['weather'][0]['icon']
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        pixmap = QPixmap()
        pixmap.loadFromData(requests.get(icon_url).content)
        self.weather_icon.setPixmap(pixmap)