import sqlite3
from dbcm import DBCM
from scrape_weather import WeatherScraper

class DBOperations:
    """ Represents a database with functions to initialize, insert data, read data, and purge the database. """
    def __init__(self, db_name='weather_data.db'):
        """ Initializes an instance of the DBOperations class. """
        self.db_name = db_name

    def initialize_db(self):
        """ Initializes a sqlite database file with the given DB name. """
        with DBCM(self.db_name) as cursor:
            try:
                cursor.execute('''create table if not exists weather
                                (id integer primary key autoincrement not null,
                                sample_date text,
                                location text,
                                min_temp real,
                                max_temp real,
                                avg_temp real,
                                unique (sample_date, location));''')
            except Exception as e:
                print("Error creating table:", e)

    def purge_data(self):
        """ Purges the database of all entries. """
        with DBCM(self.db_name) as cursor:
            try:
                cursor.execute('''delete from weather''')
            except Exception as e:
                print("Error purging database:", e)

    def save_data(self, weather_data, location="Winnipeg, MB"):
        """ Accepts a dictionary of weather data and inserts the given values into the database. """
        with DBCM(self.db_name) as cursor:
            try:
                for date, data in weather_data.items():
                    max_temp = data.get('Max')
                    min_temp = data.get('Min')
                    avg_temp = data.get('Mean')
                    cursor.execute('''
                        INSERT OR IGNORE INTO weather (sample_date, location, min_temp, max_temp, avg_temp)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (date, location, min_temp, max_temp, avg_temp))
            except Exception as e:
                print("Error inserting data:", e)

    def fetch_data(self):
        """ Returns all rows from the database. """
        with DBCM(self.db_name) as cursor:
            try:
                cursor.execute("select * from weather")
                rows = cursor.fetchall()
                return rows
            except Exception as e:
                print("Error fetching from weather:", e)
                return e

if __name__ == "__main__":
    weather_scraper = WeatherScraper()
    db_ops = DBOperations()

    weather_data = weather_scraper.scrape_weather_data()

    db_ops.initialize_db()
    db_ops.purge_data()
    db_ops.save_data(weather_data, "Winnipeg, MB")
