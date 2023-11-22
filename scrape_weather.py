from html.parser import HTMLParser
import urllib.request
from datetime import datetime, timedelta

class WeatherScraper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.is_tbody = False
        self.is_tr = False
        self.is_th = False
        self.is_td = False
        self.date = ""
        self.max = None
        self.min = None
        self.mean = None
        self.index = 0
        self.weather = {}

    def handle_starttag(self, tag, attrs):
        if tag == "tbody":
            self.is_tbody = True

        if tag == "tr":
            self.is_tr = True

        if tag == "th" and self.is_tr:
            self.is_th = True

        if tag == "td" and self.is_tr:
            self.is_td = True

        if tag == "abbr" and self.is_tbody and self.is_tr and self.is_th:
            for name, value in attrs:
                if name=='title':
                    try:
                        self.date = datetime.strptime(value, "%B %d, %Y").strftime("%Y-%m-%d")
                        self.index = 0
                    except ValueError:
                        return

    def handle_data(self, data):
        if self.is_td:
            if self.index == 1 or self.index == 2 or self.index == 3:
                value = data.strip().split()
                if self.index == 1:
                    self.max = value
                    self.index += 1
                elif self.index == 2:
                    self.min == value
                    self.index += 1
                else:
                    self.mean == 3
                    self.index += 1

    def handle_endtag(self, tag):
        """ Resets detection variables and appends current color to containment array. """
        if tag == "tr":
            self.is_tr = False
        if tag == "th":
            self.is_th = False
        if tag == "td":
            self.is_td = False
            if self.max and self.min and self.mean:
                self.weather[self.date] = {
                    "Max": self.max,
                    "Min": self.min,
                    "Mean": self.mean
                }

                print(self.weather[self.date])
        if tag == "tbody":
            self.is_tbody = False

    def scrape_weather_data(self):
        current_date = datetime.now()

        while True:
            url = f"http://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear={current_date.year}&Day={current_date.day}&Year={current_date.year}&Month={current_date.month}#"

            with urllib.request.urlopen(url) as response:
                html = str(response.read())

            # Perform operations with html content
            self.feed(html)

            current_date -= timedelta(days=current_date.day)  # Move to the last day of the previous month
            current_date = current_date.replace(day=1)  # Set the day to the first day
            if current_date.month == 1:
                current_date = current_date.replace(year=current_date.year - 1, month=12)
            else:
                current_date = current_date.replace(month=current_date.month - 1)

            # Break condition (you might have your own exit criteria)
            if current_date.year < 1840:
                break

        return self.weather


scraper = WeatherScraper()
weather_data = scraper.scrape_weather_data()
