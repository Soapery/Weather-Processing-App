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
        self.main = None
        self.db_ops = DBOperations()
        self.weather_scraper = WeatherScraper()
        self.plot_operations = PlotOperations()
        self.weather_data = self.db_ops.fetch_data()
        self.first_date = ""
        self.last_date = ""
        self.db_state = ""
        self.main_title = ""
        self.db_present = False
        self.get_first_and_last_date()

        options = [
            ("Download Weather Data", self.download_weather_data),
        ]

        if self.db_present:
            options.append(("Update Weather Data", self.update_weather_data))
            options.append(("Generate Box Plot", self.generate_box_plot))
            options.append(("Generate Line Plot", self.generate_line_plot))

        options.append(("Exit", self.exit_application))

        self.main = Menu(title=self.main_title, prompt=">>", options=options)

    def download_weather_data(self):
        """Prompts the user to confirm scraping,
        or go back to the main menu."""

        def begin_scraping(self, sub):
            """Initiates the process of scraping the Winnipeg weather site,
            going from most recent to oldest."""
            weather_data = self.weather_scraper.scrape_weather_data()
            self.db_ops.initialize_db()
            self.db_ops.purge_data()
            self.db_ops.save_data(weather_data, "Winnipeg, MB")
            self.get_first_and_last_date()

            sub.close()

        sub = Menu(
            title="Download new weather data? This process will take a while.",
            prompt=">>",
        )

        options = [
            ("Confirm", begin_scraping, {"self": self, "sub": sub}),
            ("Cancel", Menu.CLOSE),
        ]
        sub.set_options(options)

        sub.open()

    def update_weather_data(self):
        """Prompts the user to confirm updating,
        or go back to the main menu."""

        def begin_updating(self, sub):
            """Initiates the process of updating the weather data database,
            checking the date of the last record and scraping only the missing dates."""
            new_weather_data = self.weather_scraper.get_new_weather_data(
                self.weather_data
            )
            self.db_ops.save_data(new_weather_data)
            self.weather_data = self.db_ops.fetch_data()
            self.get_first_and_last_date()

            sub.close()

        sub = Menu(
            title="Update weather data?",
            prompt=">>",
        )

        options = [
            ("Confirm", begin_updating, {"self": self, "sub": sub}),
            ("Cancel", Menu.CLOSE),
        ]
        sub.set_options(options)

        sub.open()

    def generate_box_plot(self):
        """Initiates the process of generating a box plot,
        prompting the user for a start and end year."""
        boxplot_start_year = None
        boxplot_end_year = None
        first_year = int(self.first_date[:4])
        last_year = int(self.last_date[:4])

        while True:
            try:
                boxplot_start_year = int(
                    input(
                        f"Enter a starting year for your boxplot between {first_year} and {last_year}: "
                    )
                )
                if boxplot_start_year >= first_year and boxplot_start_year <= last_year:
                    break
                raise YearOutOfRangeError(
                    f"Invalid input, please enter a year between {first_year} and {last_year}."
                )
            except ValueError:
                print("Invalid input, please enter a valid number.")
            except YearOutOfRangeError:
                print(
                    f"Invalid input, please enter a year between {first_year} and {last_year}."
                )

        while True:
            try:
                boxplot_end_year = int(
                    input(
                        f"Enter an ending year for your boxplot between {first_year} and {last_year}: "
                    )
                )
                if boxplot_end_year >= first_year and boxplot_end_year <= last_year:
                    if boxplot_end_year > boxplot_start_year:
                        break
                    raise EndGreaterThanStartError(
                        f"Invalid input, please enter a year after {boxplot_start_year}."
                    )
                raise YearOutOfRangeError(
                    f"Invalid input, please enter a year between {first_year} and {last_year}."
                )
            except ValueError:
                print("Invalid input, please enter a valid number.")
            except YearOutOfRangeError as e:
                print(e)
            except EndGreaterThanStartError as e:
                print(e)

        self.plot_operations.create_boxplot(
            self.weather_data, boxplot_start_year, boxplot_end_year
        )

    def generate_line_plot(self):
        """Initiates the process of generating a line plot,
        prompting the user for a year and month."""
        lineplot_year = None
        lineplot_month = None
        first_year = int(self.first_date[:4])
        last_year = int(self.last_date[:4])
        while True:
            try:
                lineplot_year = int(
                    input(
                        f"Enter a year for your lineplot between {first_year} and {last_year}: "
                    )
                )
                if lineplot_year >= first_year and lineplot_year <= last_year:
                    break
                raise YearOutOfRangeError(
                    f"Invalid input, please enter a year between {first_year} and {last_year}."
                )
            except ValueError:
                print("Invalid input, please enter a valid number.")
            except YearOutOfRangeError as e:
                print(e)

        while True:
            try:
                lineplot_month = int(input(f"Enter a month for your lineplot (1-12): "))
                if lineplot_month >= 1 and lineplot_month <= 12:
                    break
                raise YearOutOfRangeError(
                    "Invalid input, please enter a month between 1 and 12."
                )
            except ValueError:
                print("Invalid input, please enter a valid number.")
            except YearOutOfRangeError as e:
                print(e)

        self.plot_operations.create_lineplot(
            self.weather_data, lineplot_year, lineplot_month
        )

    def get_first_and_last_date(self):
        """Gets the first and last stored dates in the database to display to the user."""
        try:
            self.first_date = str(list(self.weather_data.keys())[-1])
            self.last_date = str(list(self.weather_data.keys())[0])
            self.db_state = f"\n\nLast recorded date: {self.last_date}"
            self.main_title = f"Welcome to WeatherProcessor. Please select a function to execute. {self.db_state}"
            self.db_present = True
            if self.main is not None:
                self.main.set_title(self.main_title)
        except Exception:
            self.db_state = (
                "\n\nNo local weather data found, please initiate a download."
            )
            self.main_title = f"Welcome to WeatherProcessor. Please select a function to execute. {self.db_state}"
            self.db_present = False
            if self.main is not None:
                self.main.set_title(self.main_title)

    def exit_application(self):
        """Exits the application"""
        print("Exiting WeatherProcessor. Goodbye!")
        exit()

    def run(self):
        """Opens the menu and displays it to the menu."""
        self.main.open()


class YearOutOfRangeError(Exception):
    """Custom exception class raised when user selects a year outside of record."""


class EndGreaterThanStartError(Exception):
    """Custom exception class raised when user selects an end year less than the start"""


if __name__ == "__main__":
    WeatherProcessor().run()
