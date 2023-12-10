"""
This module contains the WeatherScraper class, which inherets the HTMLParser class.
WeatherScraper contains functions for scraping weather data for the city of Winnipeg, and returning it to the user.
"""

from html.parser import HTMLParser
import urllib.request
from datetime import datetime
from weather_logger import WeatherLogger

class WeatherScraper(HTMLParser):
    """ Represents a specialized HTMLParser used for scraping
    weather information from the city of Winnipeg. """
    def __init__(self):
        """ Initializes an instance of the WeatherScraper class. """
        super().__init__()
        self.is_tbody = False
        self.is_tr = False
        self.is_th = False
        self.is_td = False
        self.date = ""
        self.date_log = set()
        self.max = None
        self.min = None
        self.mean = None
        self.nums_checked = False
        self.index = 0
        self.complete = False
        self.weather = {}

        logger = WeatherLogger()
        self.logger = logger.get_logger()

    def handle_starttag(self, tag, attrs):
        """ Checks if the current tag is one we need to scrape data from,
        as well as checks the date of the record if applicable. """
        if tag == "tbody":
            try:
                self.is_tbody = True
            except Exception as e:
                self.logger.error("Error entering td tag: %s", e)

        if tag == "tr":
            try:
                self.is_tr = True
            except Exception as e:
                self.logger.error("Error entering td tag: %s", e)

        if tag == "th" and self.is_tr:
            try:
                self.is_th = True
            except Exception as e:
                self.logger.error("Error entering th tag: %s", e)

        if tag == "td" and self.is_tr:
            try:
                self.is_td = True
            except Exception as e:
                self.logger.error("Error entering td tag: %s", e)

        if tag == "abbr" and self.is_tbody and self.is_tr and self.is_th:
            for name, value in attrs:
                if name=='title':
                    try:
                        self.date = datetime.strptime(value, "%B %d, %Y").strftime("%Y-%m-%d")
                        if self.date in self.date_log:
                            self.complete = True
                            self.logger.info("Scraping website completed successfully.")
                            return

                        self.index = 0
                        self.date_log.add(self.date)
                    except ValueError:
                        return

    def handle_data(self, data):
        """ Parses the current tag and places
        the data in the relevant variable. """
        if self.is_td:
            if self.index == 1 or self.index == 2 or self.index == 3:
                value = str(data.strip().split()).lstrip("['").rstrip("']")
                try:
                    value = float(value)
                except ValueError:
                    value = 0.0

                if self.index == 1:
                    try:
                        self.max = value
                    except Exception as e:
                        self.logger.error("Error setting max value: %s", e)
                elif self.index == 2:
                    try:
                        self.min = value
                    except Exception as e:
                        self.logger.error("Error setting min value: %s", e)
                else:
                    try:
                        self.mean = value
                        self.nums_checked = True
                    except Exception as e:
                        self.logger.error("Error setting mean value: %s", e)

            self.index += 1

    def handle_endtag(self, tag):
        """ Resets detection variables and appends
        weather data to containment dictionary. """
        if tag == "tr":
            try:
                self.is_tr = False
            except Exception as e:
                self.logger.error("Error exiting tr tag: %s", e)

        if tag == "th":
            try:
                self.is_th = False
            except Exception as e:
                self.logger.error("Error exiting th tag: %s", e)

        if tag == "td":
            try:
                self.is_td = False
            except Exception as e:
                self.logger.error("Error exiting td tag: %s", e)

            if self.nums_checked:
                try:
                    self.weather[self.date] = {
                        "Max": self.max,
                        "Min": self.min,
                        "Mean": self.mean
                    }
                    # self.logger.info(f"{self.date}: {self.weather[self.date]}")
                    self.max = None
                    self.min = None
                    self.mean = None
                    self.nums_checked = False
                except Exception as e:
                    self.logger.error("Error saving weather data: %s", e)

        if tag == "tbody":
            try:
                self.is_tbody = False
            except Exception as e:
                self.logger.error("Error exiting tbody tag: %s", e)

    def scrape_weather_data(self):
        """ Scrapes data from the
        weather information website. """
        current_date = datetime.now()
        current_date = current_date.replace(day=1)

        try:
            while True:
                """ Loops back from the current date,
                querying the weather data website until dataset is complete. """
                url = f"http://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear={current_date.year}&Day={current_date.day}&Year={current_date.year}&Month={current_date.month}#"

                with urllib.request.urlopen(url) as response:
                    html = str(response.read())

                # Perform operations with html content
                self.feed(html)

                if current_date.month == 1:
                    current_date = current_date.replace(year=current_date.year - 1, month=12)
                else:
                    current_date = current_date.replace(month=current_date.month - 1)

                if self.complete:
                    break

                self.logger.info("Finished scraping: %s", current_date.strftime('%B - %Y'))
        except Exception as e:
            self.logger.error("Error scraping weather data: %s", e)

        return self.weather

    def get_new_weather_data(self, outdated_weather_data):
        """ Accepts a list of weather data and
        returns a list of weather data for the dates missing on the original list. """

        most_recent_date = str(list(outdated_weather_data.keys())[0])

        self.date_log.add(most_recent_date)

        new_data = self.scrape_weather_data()

        for date in list(new_data.keys()):
            if date < most_recent_date:
                del new_data[date]

        return new_data





if __name__ == "__main__":
    scraper = WeatherScraper()
    weather_data = scraper.scrape_weather_data()
    print(weather_data)
