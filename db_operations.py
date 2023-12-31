"""
This module contains the DBOperations class,
which has functions for initializing, purging, and saving data in a SQLite3 database.
This module imports the DBCM module to manage cursors and opening/closing connections.
"""

from dbcm import DBCM
from scrape_weather import WeatherScraper
from plot_operations import PlotOperations
from weather_logger import WeatherLogger
from datetime import datetime

class DBOperations:
    """ Represents a database with functions to initialize,
    insert data, read data, and purge the database. """
    def __init__(self, db_name='weather_data.sqlite'):
        """ Initializes an instance of the DBOperations class. """
        self.db_name = db_name

        logger = WeatherLogger()
        self.logger = logger.get_logger()

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

                self.logger.info("Database initialized successfully.")
            except Exception as e:
                self.logger.critical("Database initialization failed! Error: %s", e)

    def purge_data(self):
        """ Purges the database of all entries. """
        with DBCM(self.db_name) as cursor:
            try:
                cursor.execute('''delete from weather''')
                self.logger.info("Database purged successfully.")
            except Exception as e:
                self.logger.error("Database purge failed! Error: %s", e)

    def save_data(self, weather_data, location="Winnipeg, MB"):
        """ Accepts a dictionary of weather data and inserts the given values into the database. """
        with DBCM(self.db_name) as cursor:
            try:
                for date, data in weather_data.items():
                    max_temp = data.get('Max')
                    min_temp = data.get('Min')
                    avg_temp = data.get('Mean')
                    cursor.execute('''
                        INSERT OR IGNORE INTO weather
                            (sample_date, location, min_temp, max_temp, avg_temp)
                        VALUES
                            (?, ?, ?, ?, ?)
                    ''', (date, location, min_temp, max_temp, avg_temp))
                    # datetime.strptime(date, "%Y-%m-%d")
                self.logger.info("Database insert of %s items completed successfully.", len(weather_data))
            except Exception as e:
                self.logger.critical("Database insert failed! Error: %s", e)

    def fetch_data(self):
        """ Returns all rows from the database. """
        weather_data = {}

        with DBCM(self.db_name) as cursor:
            try:
                cursor.execute("select * from weather order by sample_date desc")
                rows = cursor.fetchall()

                for row in rows:
                    date = row[1]
                    min_temp = row[3]
                    max_temp = row[4]
                    avg_temp = row[5]

                    weather_data[date] = {'Min': min_temp, 'Max': max_temp, 'Mean': avg_temp}

                self.logger.info("Database rows from database \"%s\" retrieved successfully.", self.db_name)
                return weather_data
            except Exception as e:
                self.logger.error("Error fetching rows from table. Error: %s", e)
                return e

if __name__ == "__main__":
    weather_scraper = WeatherScraper()
    db_ops = DBOperations()

    weather_data = weather_scraper.scrape_weather_data()

    db_ops.initialize_db()
    db_ops.purge_data()
    db_ops.save_data(weather_data, "Winnipeg, MB")

