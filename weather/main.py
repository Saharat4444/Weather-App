import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox)
from PyQt5.QtCore import Qt 

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        # Initialize widgets
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        
        # Initialize UI layout
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")

        # Create a vertical layout and add widgets to it
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        # Set the layout for the widget
        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
            QLabel, QPushButton {
                font-family: calibri;
            }
            QLabel#city_label {
                font-size: 40px;    
                font-style: italic;  
            }
            QLineEdit#city_input {
                font-size: 40px;               
            }
            QPushButton#get_weather_button {
                font-size: 30px;  
                font-weight: bold;             
            }
            QLabel#temperature_label {
                font-size: 75px;           
            }
            QLabel#emoji_label {
                font-size: 100px;    
                font-family: "Segoe UI Emoji";        
            }
            QLabel#description_label {
                font-size: 50px;               
            }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "ca6b32078829ef60e9753e0cf6447f03"
        city = self.city_input.text()
        if not city.strip():
            QMessageBox.warning(self, "Input Error", "City name cannot be empty!")
            return

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)
            else:
                QMessageBox.warning(self, "Error", f"City not found: {city}")

        except requests.exceptions.HTTPError:
            QMessageBox.critical(self, "Error", f"HTTP Error {response.status_code}: Unable to fetch weather.")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Request Error: {e}")

    def display_weather(self, data):
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        emoji = self.get_weather_emoji(description)

        self.temperature_label.setText(f"{temp}°F")
        self.description_label.setText(description.capitalize())
        self.emoji_label.setText(emoji)

    def get_weather_emoji(self, description):
        description = description.lower()
        if "clear" in description:
            return "☀️"
        elif "cloud" in description:
            return "☁️"
        elif "rain" in description or "drizzle" in description:
            return "🌧️"
        elif "thunderstorm" in description:
            return "⛈️"
        elif "snow" in description:
            return "❄️"
        elif "mist" in description or "fog" in description:
            return "🌫️"
        else:
            return "🌍"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    Weather_App = WeatherApp()
    Weather_App.show() 
    sys.exit(app.exec_())
