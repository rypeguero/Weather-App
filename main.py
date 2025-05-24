import sys
import requests
import tkinter as tk

from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit)

from PyQt5.QtCore import Qt

from tkinter import Tk, Label, PhotoImage

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        #Start components
        self.zipcode_label = QLabel("Enter ZIP Code",self)
        self.zipcode_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather",self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self):
        #We set window title
        self.setWindowTitle("My Weather App")

        #Layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.zipcode_label)
        layout.addWidget(self.zipcode_input)
        layout.addWidget(self.get_weather_button)
        layout.addWidget(self.temperature_label)
        layout.addWidget(self.emoji_label)
        layout.addWidget(self.description_label)

        #Align labels to center
        self.setLayout(layout)
        self.zipcode_label.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        #Set object names for styling
        self.zipcode_label.setObjectName("city_label")
        self.zipcode_input.setObjectName("zipcode_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        #Styling
        self.setStyleSheet("""
        QLabel, QPushButton{
            font-family: arial black;
            font-size: 70px;  
        }
        QLabel#city_label{
            font-size: 80px;
            font-style: Times New Roman;
        }
        QLineEdit#zipcode_input{
            font-size: 40px;
        }
        QPushButton#get_weather_button{
            font-size: 50px;
            font-weight: bold;
            color: blue;
            }
        QLabel#temperature_label{
            font-size: 100px;
        }
        QLabel#emoji_label{
            font-size: 150px;
            font-family: Segoe UI Emoji;
        }
        QLabel#description_label{
            font-size: 70px;
        }
        """)
        #Connect button and input to get_weather method
        self.get_weather_button.clicked.connect(self.get_weather)
        self.zipcode_input.returnPressed.connect(self.get_weather)

    def get_weather(self):
        #get the ZIP code from input
        zipcode = self.zipcode_input.text()
        api_key = "a6f4cd2e8e2a53a80afbd3b5109f54ec"
        url = f"https://api.openweathermap.org/data/2.5/weather?zip={zipcode},&appid={api_key}"

        try:
            #Make a request to the API
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            #check if response is successful
            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError:
            #Handle HTTP errors
            match response.status_code:
                case 400:
                    self.display_error("Bad resquest\nPlease enter a valid ZIP code")
                case 401:
                    self.display_error("Unauthorized\nInvalid API key")
                case 403:
                    self.display_error("Forbidden\nYou don't have permission to access this resource")
                case 404:
                    self.display_error("Not Found\nThe resource you requested could not be found")
                case 429:
                    self.display_error("Too Many Requests\nYou have exceeded the rate limit")
                case 500:
                    self.display_error("Internal Server Error\nThe server has encountered a situation it doesn't know how to handle")
                case 502:
                    self.display_error("Bad Gateway\nThe server was acting as a gateway or proxy and received an invalid response from the upstream server")
                case 503:
                    self.display_error("Service Unavailable\nThe server is not ready to handle the request")
                case 504:
                    self.display_error("Gateway Timeout\nThe server was acting as a gateway or proxy and did not receive a timely response from the upstream server")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nA Connection error occurred")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too Many Redirects:\nThe request exceeded the configured number of maximum redirections")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"An error occurred: {req_error}")


    def display_error(self, message):
        #Display error message
        self.temperature_label.setStyleSheet("font-size: 15px; color: red;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, data):
        #Display weather information
        self.temperature_label.setStyleSheet("font-size: 75px")
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15
        temperature_f = temperature_c * 9/5 + 32
        weather_description = data["weather"][0]["description"]
        weather_id = data["weather"][0]["id"]



        self.temperature_label.setText(f"{temperature_f:.0f}°F")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)

    @staticmethod
    def get_weather_emoji(weather_id):
        #Return an emoji based on the weather ID

        if 200 <= weather_id <= 299:
            return "⛈️"
        if 300 <= weather_id <= 399:
            return "🌧️"
        if 500 <= weather_id <= 599:
            return "🌧️"
        if 600 <= weather_id <= 699:
            return "❄️"
        if 700 <= weather_id <= 799:
            return "🌫️"
        if weather_id == 800:
            return "🌞"
        if 801 <= weather_id <= 809:
            return "🌤️"
        return "🤷"


if __name__== "__main__":
    #We run the application
    app = QApplication(sys.argv)
    w = WeatherApp()
    w.show()
    sys.exit(app.exec_())