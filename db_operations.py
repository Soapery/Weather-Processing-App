import sqlite3
from dbcm import DBCM
from scrape_weather import WeatherScraper

class DBOperations:
    """ Represents a database with functions to initialize, insert data, read data, and purge the database. """
    def __init__(self, db_name='weather_data.db'):
        """ Initializes an instance of the DBOperations class. """
        self.db_name = db_name
        self.conn = None

    def initialize_db(self):
        """ Initializes a sqlite database file with the given DB name. """
        try:
            self.conn = sqlite3.connect(self.db_name)
            print("Opened database successfully.")
        except Exception as e:
            print("Error opening DB:", e)

        try:
            cursor = self.conn.cursor()
            cursor.execute('''create table if not exists weather
                            (id integer primary key autoincrement not null,
                            sample_date text,
                            location text,
                            min_temp real,
                            max_temp real,
                            avg_temp real,
                            unique (sample_date, location));''')
            self.conn.commit()
        except Exception as e:
            print("Error creating table:", e)

    def purge_data(self):
        """ Purges the database of all entries. """
        try:
            cursor = self.conn.cursor()
            cursor.execute('''delete from weather''')
            self.conn.commit()
        except Exception as e:
            print("Error purging database:", e)

    def save_data(self, weather_data, location="Winnipeg, MB"):
        """ Accepts a dictionary of weather data and inserts the given values into the database. """
        try:
            cursor = self.conn.cursor()
            for date, data in weather_data.items():
                max_temp = data.get('Max')
                min_temp = data.get('Min')
                avg_temp = data.get('Mean')
                cursor.execute('''
                    INSERT OR IGNORE INTO weather (sample_date, location, min_temp, max_temp, avg_temp)
                    VALUES (?, ?, ?, ?)
                ''', (date, location, min_temp, max_temp, avg_temp))
            self.conn.commit()
        except Exception as e:
            print("Error inserting data:", e)

    def fetch_data(self):
        """ Returns all rows from the database. """
        try:
            cursor = self.conn.cursor()
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

    with DBCM():
        db_ops.initialize_db()
        db_ops.purge_data()
        db_ops.save_data(weather_data)
        fetched_data = db_ops.fetch_data()
        print(fetched_data)
