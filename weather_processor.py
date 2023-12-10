"""
This module contains the WeatherProcessor class,
which shows the user a menu for interfacing with the functions of this application.
WeatherProcessor contains functions for starting a scraping of weather data,
prompting a database update, and generating box and line plots.
"""

from menu import Menu
from db_operations import DBOperations
from scrape_weather import WeatherScraper
from plot_operations import PlotOperations


class WeatherProcessor:
    """Represents the user interface of the application,
    and includes functions to invoke the various functions of the app."""

    def __init__(self):
        """Initializes an instance of the WeatherProcessor class
        and constructs a menu of options to present to the user."""
        self.db_ops = DBOperations()
        self.weather_scraper = WeatherScraper()
        self.plot_operations = PlotOperations()
        self.weather_data = self.db_ops.fetch_data()

        self.db_state = ""
        self.db_present = False
        try:
            self.db_state = (
                f"\n\nLast recorded date: {str(list(self.weather_data.keys())[0])}"
            )
            self.db_present = True
        except Exception:
            self.db_state = (
                "\n\nNo local weather data found, please initiate a download."
            )

        options = [
            ("Download Weather Data", self.download_weather_data),
        ]

        if self.db_present:
            options.append(("Update Weather Data", self.update_weather_data))
            options.append(("Generate Box Plot", self.generate_box_plot))
            options.append(("Generate Line Plot", self.generate_line_plot))

        title = f"Welcome to WeatherProcessor. Please select a function to execute. {self.db_state}"

        self.main = Menu(title=title, prompt=">>", options=options)

    def download_weather_data(self):
        """Prompts the user to confirm scraping,
        or go back to the main menu."""

        def begin_scraping(self):
            """Initiates the process of scraping the Winnipeg weather site,
            going from most recent to oldest. """
            weather_data = self.weather_scraper.scrape_weather_data()
            self.db_ops.initialize_db()
            self.db_ops.purge_data()
            self.db_ops.save_data(weather_data, "Winnipeg, MB")

        options = [("Confirm", begin_scraping), ("Cancel", Menu.CLOSE)]

        sub = Menu(
            title="Download new weather data? This process will take a while.",
            prompt=">>",
            options=options,
        )

        sub.open()

    def update_weather_data(self):
        """Initiates the process of updating the weather data database,
        checking the date of the last record and scraping only the missing dates."""
        print("hi")

    def generate_box_plot(self):
        """Initiates the process of generating a box plot,
        prompting the user for a start and end year."""
        print("hi")

    def generate_line_plot(self):
        """Initiates the process of generating a line plot,
        prompting the user for a year and month."""
        print("hi")

    def run(self):
        """Opens the menu and displays it to the menu."""
        self.main.open()


WeatherProcessor().run()
