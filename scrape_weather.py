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
        self.is_a = False
        self.date = ""
        self.date_log = set()
        self.max = None
        self.min = None
        self.mean = None
        self.nums_checked = False
        self.index = 0
        self.complete = False
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

        if tag == "a" and self.is_tr and self.is_td:
            self.is_a = True

        if tag == "abbr" and self.is_tbody and self.is_tr and self.is_th:
            for name, value in attrs:
                if name=='title':
                    try:
                        self.date = datetime.strptime(value, "%B %d, %Y").strftime("%Y-%m-%d")
                        if self.date in self.date_log:
                            self.complete = True
                            return
                        else:
                            self.index = 0
                            self.date_log.add(self.date)
                    except ValueError:
                        return

    def handle_data(self, data):
        if self.is_td:
            if self.index == 1 or self.index == 2 or self.index == 3:
                value = str(data.strip().split()).lstrip("['").rstrip("']")
                try:
                    value = float(value)
                except ValueError:
                    value = 0.0

                if self.index == 1:
                    self.max = value
                elif self.index == 2:
                    self.min = value
                else:
                    self.mean = value
                    self.nums_checked = True

            self.index += 1

        if self.is_a:
            if self.index == 1 or self.index == 2 or self.index == 3:
                value = data.strip().split()
                print(value)

    def handle_endtag(self, tag):
        if tag == "tr":
            self.is_tr = False
        if tag == "th":
            self.is_th = False
        if tag == "td":
            self.is_td = False
            if self.nums_checked:
                self.weather[self.date] = {
                    "Max": self.max,
                    "Min": self.min,
                    "Mean": self.mean
                }
                print(f"{self.date}: {self.weather[self.date]}")
                self.max = None
                self.min = None
                self.mean = None
                self.nums_checked = False
        if tag == "a":
            self.is_a = False
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

            if current_date.month == 1:
                current_date = current_date.replace(year=current_date.year - 1, month=12)
            else:
                current_date = current_date.replace(month=current_date.month - 1)

            # Break condition (you might have your own exit criteria)
            if self.complete:
                break

        return self.weather


scraper = WeatherScraper()
weather_data = scraper.scrape_weather_data()
print(weather_data)
