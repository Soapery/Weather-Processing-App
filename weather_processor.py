"""
This module contains the WeatherProcessor class, which shows the user a menu for interfacing with the functions of this application.
WeatherProcessor contains functions for starting a scraping of weather data, prompting a database update, and generating box and line plots.
"""

from menu import Menu
from db_operations import DBOperations

class WeatherProcessor():
    """ Represents the user interface of the application,
    and includes functions to invoke the various functions of the app. """
    def __init__(self):
        """ Initializes an instance of the WeatherProcessor class
        and constructs a menu of options to present to the user. """
        self.db_ops = DBOperations()
        self.weather_data = self.db_ops.fetch_data()

        last_date = str(list(self.weather_data.keys())[0])

        options = [
            ("Download Weather Data", self.download_weather_data),
            ("Update Weather Data", self.update_weather_data),
            ("Generate Box Plot", self.generate_box_plot),
            ("Generate Line Plot", self.generate_line_plot)
        ]

        title = f"Welcome to WeatherProcessor. Please select a function to execute.\n\nLast recorded date: {last_date}"

        self.main = Menu(
          title= title,
          prompt=">>",
          options= options
        )

    def download_weather_data(self):
        print("hi")

    def update_weather_data(self):
        print("hi")

    def generate_box_plot(self):
        print("hi")

    def generate_line_plot(self):
        print("hi")

    def run(self):
        self.main.open()

WeatherProcessor().run()